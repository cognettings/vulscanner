resource "aws_grafana_workspace" "monitoring" {
  name                     = "monitoring"
  description              = "Fluid Attacks' Universe Monitoring"
  account_access_type      = "CURRENT_ACCOUNT"
  authentication_providers = ["SAML"]
  permission_type          = "CUSTOMER_MANAGED"
  role_arn                 = aws_iam_role.grafana.arn

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_grafana_workspace_saml_configuration" "monitoring" {
  workspace_id     = aws_grafana_workspace.monitoring.id
  idp_metadata_xml = <<-EOL
    <?xml version="1.0" encoding="UTF-8"?><md:EntityDescriptor entityID="http://www.okta.com/exksbn4x8yQVybijk357" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"><md:IDPSSODescriptor WantAuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol"><md:KeyDescriptor use="signing"><ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:X509Data><ds:X509Certificate>MIIDqDCCApCgAwIBAgIGAYgm/pU9MA0GCSqGSIb3DQEBCwUAMIGUMQswCQYDVQQGEwJVUzETMBEG
    A1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU
    MBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEcMBoGCSqGSIb3DQEJ
    ARYNaW5mb0Bva3RhLmNvbTAeFw0yMzA1MTYyMzU1MzhaFw0zMzA1MTYyMzU2MzhaMIGUMQswCQYD
    VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsG
    A1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEc
    MBoGCSqGSIb3DQEJARYNaW5mb0Bva3RhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
    ggEBAJxKifGbkJzWeOAsMigtHvDNK0K86DHIKA6mawyhP0kQTmTXCXZQ4XKIqNkDOCmaKLbWo0jW
    A/l6WL+plj+IQG0qEoYqMQ4QnP+2PYqIE9+zH8EV3EDjxmSQUKBXRFjcp7wpgtYR/XiBAuAJXYvX
    mbdfw3IdzOehTC4DA17AC9SVV42MmxQdBc2zFBMVvx0da0LGZU9oWk/79rbtmdpJHqxc/FQOdTgb
    hfWp+lZenj+2mCt4BaaVf1j2MIlPmrarxZGFCAmEevd6fYHf4Jxd61jNdI9UtxoesHGrHvF8H6LV
    rTeprR84/ima0PncKekabjFu4IGtqHtthOHaQqND89sCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEA
    Y7ZonuMN/JxyePCsG7fk3dO+dfWMsJSGy7D4hlydywbOPrmMEPMH4/RP+W5AkjwbVXGF/7DABYQN
    Bf2sgfgxPpRyPIQ2T2PlJMpT3k/ZxrMaRVyv6deyV/HBbKNtJygocwzGtjHgl6zLmh7C0r0ZNN/H
    EKYgewU/FzSjFB4bVPy4tKrXYUn/CBl4dR9hf03aZUS/rvPecD6f98CaNwHnyfFR2GlovFTm/6WT
    BtOPn4M50ip3e8/6whh1qpeaTNE6mt82Es6TdsNmxcSxaQCOAjHnYETptEOJ9ZLMO1/fm64YBFB6
    9NMWrDO80t9ZnnJiPVnkPIjaEcsTXbIlnW0SmQ==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></md:KeyDescriptor><md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://fluidattacks.okta.com/app/amazonmanagedgrafanasaml/exksbn4x8yQVybijk357/sso/saml"/><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://fluidattacks.okta.com/app/amazonmanagedgrafanasaml/exksbn4x8yQVybijk357/sso/saml"/></md:IDPSSODescriptor></md:EntityDescriptor>
  EOL

  admin_role_values  = ["admin"]
  editor_role_values = ["editor"]

  name_assertion          = "displayName"
  email_assertion         = "mail"
  login_assertion         = "mail"
  role_assertion          = "role"
  login_validity_duration = 24 * 60 # 1 Day
}

resource "aws_grafana_workspace_api_key" "monitoring" {
  key_name        = "terraform"
  key_role        = "ADMIN"
  seconds_to_live = 2592000 # 30 Days
  workspace_id    = aws_grafana_workspace.monitoring.id
}

resource "grafana_folder" "monitoring" {
  uid   = "monitoring"
  title = "Monitoring"

  lifecycle {
    prevent_destroy = true
  }
}

data "grafana_dashboards" "monitoring" {}

data "grafana_dashboard" "monitoring" {
  for_each = toset([
    for dashboard in data.grafana_dashboards.monitoring.dashboards : dashboard.uid
  ])

  uid = each.value
}

resource "aws_s3_object" "grafana_backups" {
  for_each = data.grafana_dashboard.monitoring

  bucket  = aws_s3_bucket.monitoring.bucket
  key     = "grafana-backups/${each.value.id}.json"
  content = data.grafana_dashboard.monitoring[each.value.uid].config_json
}
