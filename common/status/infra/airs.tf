resource "checkly_check" "airs" {
  name                      = "WEB"
  type                      = "BROWSER"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 1

  locations = ["us-east-1"]

  script = <<-EOF
    const assert = require("chai").assert;
    const playwright = require("playwright");

    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto("https://fluidattacks.com/", {
      waitUntil: "domcontentloaded"
    });
    const title = await page.title();

    assert.equal(title, "Application security testing solutions | Fluid Attacks");
    await browser.close();
  EOF
}

resource "betteruptime_monitor" "airs" {
  check_frequency    = 180
  monitor_type       = "keyword"
  paused             = false
  pronounceable_name = "WEB"
  recovery_period    = 0
  request_timeout    = 30
  required_keyword   = "Application security testing solutions | Fluid Attacks"
  url                = "https://fluidattacks.com"
  verify_ssl         = true
}

resource "betteruptime_status_page_resource" "airs" {
  public_name            = "WEB"
  resource_id            = betteruptime_monitor.airs.id
  resource_type          = "Monitor"
  status_page_id         = betteruptime_status_page.main.id
  status_page_section_id = betteruptime_status_page_section.main.id
  widget_type            = "response_times"
}
