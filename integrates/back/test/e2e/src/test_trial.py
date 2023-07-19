# pylint: disable=import-error, too-many-locals, useless-suppression
from model import (
    Credentials,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
import utils


def test_trial_onboarding(
    driver: WebDriver,
    asm_endpoint: str,
    timeout: int,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    credentials = Credentials(user="jdoe@testcompany.com")
    utils.login(
        driver, asm_endpoint, credentials, jwt_secret, jwt_encryption_key
    )
    driver.get(f"{asm_endpoint}/home")

    assert utils.wait_for_text(driver, "Looks like", timeout)
    start_button = utils.wait_for_text(driver, "Start free trial", timeout)
    start_button.click()
    manual_button = utils.wait_for_text(
        driver, "Add your repository manually", timeout
    )
    manual_button.click()

    assert utils.wait_for_text(
        driver,
        "Provide the information of the repository you want to scan.",
        timeout,
    )
    repo_url = utils.wait_for_aria_label(driver, "input", "url", timeout)
    repo_url.send_keys("https://gitlab.com/fluidattacks/demo")
    branch = utils.wait_for_aria_label(driver, "input", "branch", timeout)
    branch.send_keys("main")
    credentials_name = utils.wait_for_aria_label(
        driver, "input", "credentials.name", timeout
    )
    credentials_name.send_keys("demo")
    credentials_user = utils.wait_for_aria_label(
        driver, "input", "credentials.user", timeout
    )
    credentials_user.send_keys("demo")
    credentials_password = utils.wait_for_aria_label(
        driver, "input", "credentials.password", timeout
    )
    credentials_password.send_keys("demo")
    environment = utils.wait_for_aria_label(driver, "input", "env", timeout)
    environment.send_keys("production")
    has_exclusions = utils.wait_for_id(driver, "hasExclusions-no", timeout)
    has_exclusions.click()
    check_access_button = utils.wait_for_text(driver, "Check access", timeout)
    check_access_button.click()
    start_trial_button = utils.wait_for_text(driver, "Start scanning", timeout)
    start_trial_button.click()

    close_button = utils.wait_for_id(driver, "welcome-close", timeout)
    close_button.click()

    assert utils.wait_for_text(
        driver,
        "We are testing your application to find vulnerabilities",
        timeout,
    )
