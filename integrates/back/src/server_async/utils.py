from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
)
import base64
from contextlib import (
    suppress,
)
from custom_utils.string import (
    boxify,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.types import (
    Item,
)
from io import (
    BytesIO,
)
import json
import os
from s3.resource import (
    get_s3_resource,
)
from starlette.datastructures import (
    UploadFile,
)
import tempfile
from tempfile import (
    SpooledTemporaryFile,
)
from typing import (
    Any,
)
import yaml
from yaml.reader import (
    ReaderError,
)

# Constants
DUMMY_IMG: Image = Image.new("RGB", (0, 0))
DUMMY_DRAWING: ImageDraw = ImageDraw.Draw(DUMMY_IMG)


async def get_config(
    execution_id: str,
    config_path: str | None = None,
) -> Item:
    # config_path is useful to test this flow locally
    if config_path is not None:
        with open(config_path, "rb") as config_file:
            return yaml.safe_load(config_file)
    s3_client = await get_s3_resource()
    print(f"configs/{execution_id}.yaml")
    with tempfile.NamedTemporaryFile(
        prefix="integrates_get_config_", delete=True
    ) as temp:
        await s3_client.download_fileobj(
            "machine.data",
            f"configs/{execution_id}.yaml",
            temp,
        )

        temp.seek(0)
        return yaml.safe_load(temp)


@retry_on_exceptions(
    exceptions=(ClientPayloadError,),
    sleep_seconds=1,
)
async def get_sarif_log(
    execution_id: str,
    sarif_path: str | None = None,
) -> Item | None:
    # sarif_path is useful to test this flow locally
    if sarif_path is not None:
        with open(sarif_path, "rb") as sarif_file:
            return yaml.safe_load(sarif_file)
    s3_client = await get_s3_resource()
    with tempfile.NamedTemporaryFile(
        prefix="integrates_get_sarif_log_", delete=True
    ) as temp:
        await s3_client.download_fileobj(
            "machine.data",
            f"results/{execution_id}.sarif",
            temp,
        )

        temp.seek(0)
        try:
            return yaml.safe_load(
                temp.read().decode(encoding="utf-8").replace("x0081", "")
            )
        except ReaderError:
            return None


def get_input_url(vuln: Item, repo_nickname: str | None = None) -> str:
    url: str
    if vuln["properties"].get("has_redirect", False):
        url = vuln["properties"]["original_url"]
    else:
        url = vuln["locations"][0]["physicalLocation"]["artifactLocation"][
            "uri"
        ]
    while url.endswith("/"):
        url = url.rstrip("/")

    if repo_nickname:
        return f"{url} ({repo_nickname})"
    return url


def clarify_blocking(image: Image, ratio: float) -> Image:
    image_mask: Image = image.convert("L")
    image_mask_pixels = image_mask.load()

    image_width, image_height = image_mask.size

    for i in range(image_width):
        for j in range(image_height):
            if image_mask_pixels[i, j]:
                image_mask_pixels[i, j] = int(ratio * 0xFF)

    image.putalpha(image_mask)

    return image


async def to_png(*, string: str, margin: int = 25) -> UploadFile:
    font = ImageFont.truetype(
        font=os.environ["SKIMS_ROBOTO_FONT"],
        size=18,
    )
    watermark: Image = clarify_blocking(
        image=Image.open(os.environ["SKIMS_FLUID_WATERMARK"]),
        ratio=0.15,
    )
    # Make this image rectangular
    string = boxify(string=string)

    # This is the number of pixes needed to draw this text, may be big
    size: tuple[int, int] = DUMMY_DRAWING.textsize(string, font=font)
    size = (
        size[0] + 2 * margin,
        size[1] + 2 * margin,
    )
    watermark_size: tuple[int, int] = (
        size[0] // 2,
        watermark.size[1] * size[0] // watermark.size[0] // 2,
    )
    watermark_position: tuple[int, int] = (
        (size[0] - watermark_size[0]) // 2,
        (size[1] - watermark_size[1]) // 2,
    )

    # Create an image with the right size to fit the snippet
    #  and resize it to a common resolution
    img: Image = Image.new("RGB", size, (0xFF, 0xFF, 0xFF))

    drawing: ImageDraw = ImageDraw.Draw(img)
    drawing.multiline_text(
        xy=(margin, margin),
        text=string,
        fill=(0x33, 0x33, 0x33),
        font=font,
    )

    watermark = watermark.resize(watermark_size)
    img.paste(watermark, watermark_position, watermark)

    stream: BytesIO = BytesIO()

    img.save(stream, format="PNG")

    stream.seek(0)

    file_object = UploadFile(
        filename="evidence",
        content_type="image/png",
        # pylint: disable-next=consider-using-with
        file=SpooledTemporaryFile(mode="wb"),  # type: ignore
    )
    await file_object.write(stream.read())
    await file_object.seek(0)
    return file_object


def decode_sqs_message(message: Any) -> str:
    with suppress(json.JSONDecodeError):
        return json.loads(message.body)["execution_id"]
    return json.loads(
        base64.b64decode(
            json.loads(base64.b64decode(message.body).decode())["body"]
        ).decode()
    )["id"]


def delete_message(queue: Any, message: Any) -> None:
    queue.delete_messages(
        Entries=[
            {
                "Id": message.message_id,
                "ReceiptHandle": message.receipt_handle,
            },
        ]
    )


def was_input_on_sarif(vuln_props: dict) -> bool:
    if vuln_props["kind"].lower() == "dast" or (
        vuln_props["kind"].lower() == "cspm"
        and vuln_props["technique"].lower() == "dast"
    ):
        return True
    return False


def was_lines_on_sarif(vuln_props: dict) -> bool:
    if vuln_props["kind"].lower() in {"sast", "sca"} or (
        vuln_props["kind"].lower() == "cloud"
        and vuln_props["technique"].lower() in {"asast", "bsast"}
    ):
        return True
    return False
