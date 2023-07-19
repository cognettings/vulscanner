# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
import re
from selenium.common.exceptions import (
    WebDriverException,
)
from selenium.webdriver.common.by import (
    By,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.support import (
    expected_conditions as ec,
)
from selenium.webdriver.support.wait import (
    WebDriverWait,
)
import utils


def test_others_login_screen(
    driver: WebDriver, asm_endpoint: str, timeout: int
) -> None:
    # Enter login screen
    driver.get(asm_endpoint)
    assert utils.wait_for_id(
        driver,
        "login-auth",
        timeout,
    )

    # Validate that images load correctly
    containers = driver.find_elements(By.CLASS_NAME, "comp-container")

    images_urls = [
        url
        for url in [
            element.value_of_css_property("background-image")
            for element in containers
        ]
        if url != "none"
    ]

    urls = [
        result.group(1)
        for result in [
            re.search(r'url\("([^"]+)"\)', url) for url in images_urls if url
        ]
        if result
    ]

    assert len(urls) == 5
    for url in urls:
        try:
            driver.get(url)
            assert driver.find_element(By.CSS_SELECTOR, "img")
        except WebDriverException as exc:
            assert False, exc


def test_others_dashboard(
    driver: WebDriver,
    credentials: Credentials,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    # Login
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )

    # Enter dashboard
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")
    assert utils.wait_for_text(
        driver,
        "Exposure management over time",
        timeout,
    )

    logo = driver.find_element(By.TAG_NAME, "img")
    driver.get(logo.get_attribute("src"))
    assert WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located((By.TAG_NAME, "svg"))
    )
