# pylint: disable=import-error, useless-suppression
from datetime import (
    datetime,
    timedelta,
)
from model import (
    Credentials,
)
from random import (
    randint,
)
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import (
    By,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.remote.webelement import (
    WebElement,
)
from selenium.webdriver.support import (
    expected_conditions as ec,
)
from selenium.webdriver.support.wait import (
    WebDriverWait,
)
from session_token import (
    calculate_hash_token,
    encode_token,
)


def wait_for_id(driver: WebDriver, text: str, timeout: int) -> WebElement:
    return WebDriverWait(
        driver,
        timeout,
        ignored_exceptions=[StaleElementReferenceException],
    ).until(
        ec.visibility_of_element_located(
            (
                By.ID,
                text,
            )
        )
    )


def wait_for_text(driver: WebDriver, text: str, timeout: int) -> WebElement:
    return WebDriverWait(
        driver,
        timeout,
        ignored_exceptions=[StaleElementReferenceException],
    ).until(
        ec.presence_of_all_elements_located(
            (
                By.XPATH,
                f"//*[text()[contains(., '{text}')]]",
            )
        )
    )[
        -1
    ]


def wait_for_aria_label(
    driver: WebDriver, element: str, text: str, timeout: int
) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located(
            (
                By.XPATH,
                f"//{element}[@aria-label='{text}']",
            )
        )
    )


def wait_for_aria_label_by_parent(
    *,
    driver: WebDriver,
    parent_id: str,
    parent_element: str,
    element: str,
    text: str,
    timeout: int,
) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        ec.visibility_of_element_located(
            (
                By.XPATH,
                f"//{parent_element}[@id='{parent_id}']"
                + f"//{element}[@aria-label='{text}']",
            )
        )
    )


def wait_for_class_name(
    driver: WebDriver, text: str, timeout: int
) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((By.CLASS_NAME, text))
    )


def wait_for_hide_text(
    driver: WebDriver, text: str, timeout: int
) -> WebElement:
    return WebDriverWait(driver, timeout).until_not(
        ec.presence_of_element_located(
            (
                By.XPATH,
                f"//*[text()[contains(., '{text}')]]",
            )
        )
    )


def wait_for_name(driver: WebDriver, text: str, timeout: int) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located(
            (
                By.NAME,
                text,
            )
        )
    )


def wait_for_text_to_click(
    driver: WebDriver, text: str, timeout: int
) -> WebElement:
    return WebDriverWait(
        driver,
        timeout,
        ignored_exceptions=[StaleElementReferenceException],
    ).until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                f"//*[text()[contains(., '{text}')]]",
            )
        )
    )


def rand_name(prefix: str) -> str:
    return f"{prefix}-{randint(0, 1000)}"


def login(
    driver: WebDriver,
    asm_endpoint: str,
    credentials: Credentials,
    jwt_secret: str,
    jwt_encryption_key: str,
) -> None:
    driver.get(asm_endpoint)
    jti = calculate_hash_token()["jti"]
    expiration_time = int(
        (datetime.utcnow() + timedelta(seconds=1800)).timestamp()
    )
    jwt_token: str = encode_token(
        expiration_time=expiration_time,
        jwt_encryption_key=jwt_encryption_key,
        jwt_secret=jwt_secret,
        payload=dict(
            user_email=credentials.user,
            first_name="Test",
            last_name="Session",
            jti=jti,
        ),
        subject="test_e2e_session",
    )

    driver.add_cookie(
        {
            "name": "integrates_session",
            "value": jwt_token,
        }
    )
    # cookie bot dialog is interfering with some tests
    dismiss_tour(driver, "CybotCookiebotDialogBodyButtonAccept")


def dismiss_tour(driver: WebDriver, close_btn_id: str) -> None:
    try:
        close_btn = wait_for_id(
            driver,
            close_btn_id,
            timeout=5,
        )
        close_btn.click()
    except TimeoutException:
        pass


def dismiss_tour_by_class_name(
    driver: WebDriver, close_btn_class_name: str
) -> None:
    try:
        close_btn = wait_for_class_name(
            driver,
            close_btn_class_name,
            timeout=5,
        )
        close_btn.click()
    except TimeoutException:
        pass


def click_button_given_its_xpath(
    driver: WebDriver, close_btn_xpath: str
) -> None:
    try:
        close_btn = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, close_btn_xpath))
        )
        close_btn.click()
    except TimeoutException:
        pass
