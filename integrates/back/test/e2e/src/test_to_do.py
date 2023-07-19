# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
import utils


def test_todo_locations_drafts(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )
    driver.get(
        f"{asm_endpoint}/todos"  # noqa: E501 pylint: disable=line-too-long
    )
    assert utils.wait_for_id(driver, "verification", timeout)
    locations_drafts_tab = utils.wait_for_id(driver, "locationDrafts", timeout)
    locations_drafts_tab.click()

    vulnerability = utils.wait_for_text_to_click(
        driver,
        "universe/universe/path/to/file3.ext",
        timeout,
    )
    vulnerability.click()
    assert driver.current_url.endswith(
        "/location-drafts/08717ec8-53a4-409c-aeb3-883b8c0a2d82"
    )
    close = utils.wait_for_id(
        driver,
        "modal-close",
        timeout,
    )
    close.click()
    assert driver.current_url.endswith("/location-drafts")
