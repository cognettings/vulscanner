resource "checkly_check" "integrates_web" {
  name                      = "PLATFORM"
  type                      = "BROWSER"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 3

  locations = ["us-east-1"]

  script = <<-EOF
    const assert = require("chai").assert;
    const playwright = require("playwright");

    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto("https://app.fluidattacks.com");
    const title = await page.title();

    assert.equal(title, "Platform | Fluid Attacks");
    await browser.close();
  EOF
}

resource "checkly_check" "integrates_api" {
  name                      = "API"
  type                      = "API"
  activated                 = true
  frequency                 = 1
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 4

  locations = ["us-east-1"]

  request {
    url              = "https://app.fluidattacks.com/api"
    follow_redirects = true
    body_type        = "GRAPHQL"
    method           = "POST"

    headers = {
      authorization = "Bearer {{INTEGRATES_API_TOKEN}}"
    }

    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "narrabri"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "imamura"
    }

    body = <<-EOF
      query ChecklyApiCheck {
        me {
          organizations {
            name
          groups {
            name
          }
        }
          remember
        }
        organization(organizationId: "ORG#0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa") {
          userRole
          groups {
            name
          }
        }
        group(groupName: "narrabri") {
          permissions
          findings {
            vulnerabilitiesConnection(
              state: VULNERABLE
            ) {
                edges {
                    node {
                        id
                        where
                    }
                }
            }
          }
        }
      }
    EOF
  }
}

resource "checkly_check" "forces_api" {
  name                      = "AGENT"
  type                      = "API"
  activated                 = true
  frequency                 = 1
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 5

  locations = ["us-east-1"]

  request {
    url              = "https://app.fluidattacks.com/api"
    follow_redirects = true
    body_type        = "GRAPHQL"
    method           = "POST"

    headers = {
      authorization = "Bearer {{INTEGRATES_API_TOKEN}}"
    }

    assertion {
      source     = "STATUS_CODE"
      comparison = "EQUALS"
      target     = "200"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "APPROVED"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "UNTREATED"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "VULNERABLE"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "bwapp"
    }

    body = <<-EOF
      query ChecklyForcesCheck {
        group(groupName: "narrabri") {
          findings {
            id
            currentState
            title
            status
            severity {
              exploitability
            }
            severityScore
          }
          forcesVulnerabilities {
            edges {
              node {
                findingId
                state
                treatmentStatus
                vulnerabilityType
                where
                severity
                specific
                reportDate
                rootNickname
                zeroRisk
              }
            }
          }
        }
      }
    EOF
  }
}

resource "betteruptime_monitor" "integrates_web" {
  check_frequency    = 180
  monitor_type       = "keyword"
  paused             = false
  pronounceable_name = "PLATFORM"
  recovery_period    = 0
  request_timeout    = 30
  required_keyword   = "Platform | Fluid Attacks"
  url                = "https://app.fluidattacks.com"
  verify_ssl         = true
}

resource "betteruptime_status_page_resource" "integrates_web" {
  public_name            = "PLATFORM"
  resource_id            = betteruptime_monitor.integrates_web.id
  resource_type          = "Monitor"
  status_page_id         = betteruptime_status_page.main.id
  status_page_section_id = betteruptime_status_page_section.main.id
  widget_type            = "response_times"
}

resource "betteruptime_monitor" "machine" {
  check_frequency    = 180
  monitor_type       = "keyword"
  paused             = false
  pronounceable_name = "MACHINE"
  recovery_period    = 0
  request_timeout    = 30
  required_keyword   = "Platform | Fluid Attacks"
  url                = "https://app.fluidattacks.com"
  verify_ssl         = true
}

resource "betteruptime_status_page_resource" "machine" {
  public_name            = "MACHINE"
  resource_id            = betteruptime_monitor.machine.id
  resource_type          = "Monitor"
  status_page_id         = betteruptime_status_page.main.id
  status_page_section_id = betteruptime_status_page_section.main.id
  widget_type            = "response_times"
}

resource "betteruptime_monitor" "integrates_api" {
  check_frequency    = 180
  http_method        = "POST"
  monitor_type       = "keyword"
  paused             = false
  pronounceable_name = "API"
  recovery_period    = 0
  request_body = jsonencode({
    query = <<-EOF
      query BetterUptimeApiCheck {
        me {
          organizations {
            groups {
              name
            }
            name
          }
          remember
        }
        organization(organizationId: "ORG#0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa") {
          groups {
            name
          }
          userRole
        }
        group(groupName: "narrabri") {
          permissions
          findings {
            vulnerabilitiesConnection(state: VULNERABLE) {
              edges {
                node {
                  id
                  where
                }
              }
            }
          }
        }
      }
    EOF
  })
  request_headers = [
    { name = "Authorization", value = "Bearer ${var.envIntegratesApiToken}" },
    { name = "Content-Type", value = "application/json" },
  ]
  request_timeout  = 30
  required_keyword = "narrabri"
  url              = "https://app.fluidattacks.com/api"
  verify_ssl       = true
}

resource "betteruptime_status_page_resource" "integrates_api" {
  public_name            = "API"
  resource_id            = betteruptime_monitor.integrates_api.id
  resource_type          = "Monitor"
  status_page_id         = betteruptime_status_page.main.id
  status_page_section_id = betteruptime_status_page_section.main.id
  widget_type            = "response_times"
}

resource "betteruptime_monitor" "forces_api" {
  check_frequency    = 180
  http_method        = "POST"
  monitor_type       = "keyword"
  paused             = false
  pronounceable_name = "AGENT"
  recovery_period    = 0
  request_body = jsonencode({
    query = <<-EOF
      query BetterUptimeForcesCheck {
        group(groupName: "narrabri") {
          findings {
            currentState
            id
            severity {
              exploitability
            }
            severityScore
            status
            title
          }
          forcesVulnerabilities {
            edges {
              node {
                findingId
                reportDate
                rootNickname
                severity
                specific
                state
                treatmentStatus
                vulnerabilityType
                where
                zeroRisk
              }
            }
          }
        }
      }
    EOF
  })
  request_headers = [
    { name = "Authorization", value = "Bearer ${var.envIntegratesApiToken}" },
    { name = "Content-Type", value = "application/json" },
  ]
  request_timeout  = 30
  required_keyword = "APPROVED"
  url              = "https://app.fluidattacks.com/api"
  verify_ssl       = true
}

resource "betteruptime_status_page_resource" "forces_api" {
  public_name            = "AGENT"
  resource_id            = betteruptime_monitor.forces_api.id
  resource_type          = "Monitor"
  status_page_id         = betteruptime_status_page.main.id
  status_page_section_id = betteruptime_status_page_section.main.id
  widget_type            = "response_times"
}
