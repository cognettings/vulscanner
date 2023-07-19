# pylint: disable=import-error, useless-suppression, too-many-arguments
from model import (
    Credentials,
)
from selenium.common.exceptions import (
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import (
    WebDriver,
)
from selenium.webdriver.support.select import (
    Select,
)
import utils
import uuid

EXPECTED_MANY_GROUPS_CHARTS: list[str] = [
    "Remediation rate benchmark",
    "Mean time to remediate (MTTR) benchmark",
    "Exposure over time",
    "Exposure by type",
    "Exposure by group",
    "Exposure benchmark",
    "Exposure management over time",
    "Exposure management over time (%)",
    "Exposure trends by vulnerability category",
    "Vulnerabilities treatment",
    "Remediation rate",
    "Total types",
    "Days until zero exposure",
    "Vulnerabilities with no treatment",
    "Vulnerabilities being re-attacked",
    "Days since last remediation",
    "Sprint exposure increment",
    "Sprint exposure decrement",
    "Sprint exposure change overall",
    "Total vulnerabilities",
    "Open vulnerabilities",
    "Active resources distribution",
    "Vulnerabilities by tag",
    "Vulnerabilities by level",
    "Accepted vulnerabilities by user",
    "Unsolved events by group",
    "Distribution of vulnerabilities by group",
    "Vulnerability types by group",
    "Open vulnerability types by group",
    "Oldest vulnerability types",
    "Vulnerabilities by group",
    "Open vulnerabilities by group",
    "Undefined treatment by group",
    "Report technique",
    "Vulnerabilities by assignment",
    "Status of assigned vulnerabilities",
    "Accepted vulnerabilities by CVSS severity",
    "Exposure by assignee",
    "Files with open vulnerabilities in the last 20 weeks",
    "Mean time to remediate (MTTR) by CVSS severity",
    "Overall availability of groups",
    "Days since groups are failing",
    "Mean time to request reattacks",
    "Tags by groups",
]


def test_org_analytics(
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

    # Enter Analytics
    driver.get(f"{asm_endpoint}/orgs/okada/analytics")

    for expected_chart in EXPECTED_MANY_GROUPS_CHARTS:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3_30&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3_90&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphic?documentName=mttrBenchmarkingCvssf&"
        "documentType=barChart&entity=organization&generatorName=generic&"
        "generatorType=c3&height=320&subject=ORG%2338eb8f25-7945-4173-ab6e"
        "-0af4ad8b7ef3&width=1055"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphics-for-organization?reportMode=true&"
        "bgChange=true&organization=ORG%2333c08ebd-2068-47e7-9673-e1aa03dc9448"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphics-for-group?reportMode=true&"
        "bgChange=true&group=unittesting"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )

    driver.get(
        f"{asm_endpoint}/graphics-for-portfolio?reportMode=true&"
        "bgChange=true&portfolio=ORG%2338eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
        "PORTFOLIO%23test-groups"
    )
    assert utils.wait_for_id(
        driver,
        "root",
        timeout,
    )


def test_org_groups(
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

    # Add group, add some randomness to allow
    # retry without group already exist error
    group_name = "akame" + str(uuid.uuid4())[:5]
    group_description: str = "test-group-description"
    driver.get(f"{asm_endpoint}/orgs/okada/groups")
    add_group = utils.wait_for_id(
        driver,
        "add-group",
        timeout,
    )
    add_group.click()
    try:
        close_tour = utils.wait_for_aria_label_by_parent(
            driver=driver,
            parent_id="react-joyride-step-0",
            parent_element="div",
            element="button",
            text="Skip",
            timeout=3,
        )
        close_tour.click()
        add_group.click()
    except TimeoutException:
        pass
    name = utils.wait_for_id(driver, "add-group-name", timeout)
    name.send_keys(group_name)
    description = utils.wait_for_id(driver, "add-group-description", timeout)
    description.send_keys(group_description)
    proceed = utils.wait_for_id(
        driver,
        "add-group-confirm",
        timeout,
    )
    proceed.click()
    assert utils.wait_for_id(
        driver,
        "successgroup created successfully",
        10,
    )

    # delete the group
    driver.get(f"{asm_endpoint}/orgs/okada/groups/{group_name}/scope")
    assert utils.wait_for_id(driver, "resources", timeout)
    utils.click_button_given_its_xpath(
        driver, '//*[@id="resources"]/div[3]/div[5]/div/button'
    )
    utils.wait_for_name(driver, "confirmation", timeout).send_keys(group_name)
    Select(utils.wait_for_name(driver, "reason", timeout)).select_by_value(
        "TR_CANCELLED"
    )
    utils.wait_for_name(driver, "comments", timeout).send_keys(
        "Delete the group to allow retry on fail"
    )
    utils.wait_for_id(driver, "modal-confirm", timeout).click()


def test_org_members(
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

    driver.get(f"{asm_endpoint}/orgs/okada/members")
    assert utils.wait_for_text(
        driver,
        "continuoushacking@gmail.com",
        timeout,
    )

    # In authors
    utils.wait_for_id(driver, "addUser", timeout).click()
    utils.wait_for_name(driver, "email", timeout).send_keys("dev@dev.com")
    Select(utils.wait_for_name(driver, "role", timeout)).select_by_value(
        "USER"
    )
    utils.wait_for_text(driver, "Confirm", timeout).click()
    assert utils.wait_for_text(driver, "dev@dev.com", timeout)
    utils.click_button_given_its_xpath(
        driver,
        '//*[@id="successan invitation email'
        ' will be sent to dev@dev.com"]/button/svg',
    )
    try:
        utils.wait_for_id(driver, "addUser", 5).click()
    except TimeoutError:
        utils.wait_for_text(driver, "modal-confirm", timeout).click()
        utils.wait_for_id(driver, "addUser", 5).click()
    utils.wait_for_name(driver, "email", timeout).send_keys(
        "dev.test@fluidattacks.com"
    )
    Select(utils.wait_for_name(driver, "role", timeout)).select_by_value(
        "USER"
    )
    confirm = utils.wait_for_text(driver, "Confirm", timeout)
    confirm.click()
    assert utils.wait_for_text(driver, "Confirm invitation", timeout)
    utils.wait_for_text(driver, "Confirm", timeout).click()
    utils.click_button_given_its_xpath(
        driver,
        '//*[@id="successan invitation email'
        ' will be sent to dev.test@fluidattacks.com"]/button/svg',
    )
    assert utils.wait_for_text(driver, "dev.test@fluidattacks.com", timeout)


def test_org_standard_compliance(
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

    # Enter compliance
    driver.get(f"{asm_endpoint}/orgs/okada/compliance")

    assert utils.wait_for_text(
        driver,
        "Organization compliance",
        timeout,
    )
    assert utils.wait_for_text(
        driver,
        "Standard with lowest compliance",
        timeout,
    )
    standards_button = utils.wait_for_text(
        driver,
        "Standards",
        timeout,
    )
    standards_button.click()
    assert utils.wait_for_text(
        driver,
        "Unfulfilled standards",
        timeout,
    )
    assert utils.wait_for_text(
        driver,
        "Requirement",
        timeout,
    )
    assert utils.wait_for_text(
        driver,
        "Generate report",
        timeout,
    )


def test_org_portfolios(
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

    # Enter portfolio
    driver.get(f"{asm_endpoint}/orgs/okada/portfolios")
    test_groups = utils.wait_for_text(
        driver,
        "test-groups",
        timeout,
    )
    test_groups.click()
    for expected_chart in EXPECTED_MANY_GROUPS_CHARTS:
        assert utils.wait_for_text(
            driver,
            expected_chart,
            timeout,
        )
