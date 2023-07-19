# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
import utils


def test_api_credentials(
    driver: WebDriver,
    credentials: Credentials,  # pylint: disable=unused-argument
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,  # pylint: disable=unused-argument
    jwt_encryption_key: str,  # pylint: disable=unused-argument
) -> None:
    # Go to API playground
    driver.get(f"{asm_endpoint}/api")

    # Wait for API playground to load
    assert utils.wait_for_id(
        driver,
        "graphiql",
        timeout,
    )
