resource "checkly_dashboard" "main" {
  custom_url      = "fluidattacks"
  custom_domain   = "status.fluidattacks.com"
  favicon         = "https://res.cloudinary.com/fluid-attacks/image/upload/v1669232201/airs/favicon-2022.png"
  link            = "https://fluidattacks.com"
  logo            = "https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1619554789/airs/logo-fluid-attacks-light_lsckin.webp"
  header          = "Status page | Fluid Attacks"
  refresh_rate    = 60
  paginate        = true
  pagination_rate = 60
  hide_tags       = true
  width           = "FULL"

  tags = [
    "production",
  ]
}

resource "betteruptime_status_page" "main" {
  company_name  = "Fluid Attacks"
  company_url   = "https://fluidattacks.com"
  contact_url   = "mailto:help@fluidattacks.com"
  custom_domain = "status.fluidattacks.com"
  design        = "v2"
  layout        = "horizontal"
  logo_url      = "https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1619554789/airs/logo-fluid-attacks-light_lsckin.webp"
  subdomain     = "fluid-attacks"
  theme         = "light"
  timezone      = "Bogota"
}

resource "betteruptime_status_page_section" "main" {
  name           = "Current status by service"
  status_page_id = betteruptime_status_page.main.id
}

output "betteruptime_status_page_id_fluidattacks" {
  value = betteruptime_status_page.main.id
}
