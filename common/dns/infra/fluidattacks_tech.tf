resource "cloudflare_zone" "fluidattacks_tech" {
  account_id = var.cloudflareAccountId
  zone       = "fluidattacks.tech"
}

resource "cloudflare_zone_settings_override" "fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id

  settings {
    always_online            = "on"
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    brotli                   = "on"
    browser_check            = "on"
    cache_level              = "aggressive"
    email_obfuscation        = "on"
    hotlink_protection       = "on"
    ip_geolocation           = "on"
    ipv6                     = "on"
    opportunistic_encryption = "on"
    min_tls_version          = "1.2"
    ssl                      = "flexible"
    tls_1_3                  = "zrt"
    universal_ssl            = "on"
    challenge_ttl            = 1800

    minify {
      css  = "on"
      html = "on"
      js   = "on"
    }

    security_header {
      enabled            = true
      include_subdomains = true
      nosniff            = false
      max_age            = 31536000
      preload            = true
    }
  }
}

resource "cloudflare_zone_dnssec" "fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
}

# Workers

resource "cloudflare_worker_script" "headers" {
  name    = "makes_headers"
  content = data.local_file.headers.content
}

resource "cloudflare_worker_route" "go_headers" {
  zone_id     = cloudflare_zone.fluidattacks_tech.id
  pattern     = "go.${cloudflare_zone.fluidattacks_tech.zone}/*"
  script_name = cloudflare_worker_script.headers.name
}

# CNAME Recordds

resource "cloudflare_record" "www_fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "www.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_tech.zone
  proxied = true
}

resource "cloudflare_record" "help" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "help.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "fluidattacks.zendesk.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "rebrandly" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "go.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "rebrandlydomain.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "announcekit" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "news.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "cname.announcekit.app"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "gd_domainconnect" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_domainconnect.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "_domainconnect.gd.domaincontrol.com"
  proxied = true
}

resource "cloudflare_record" "secureserver" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "email.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "email.secureserver.net"
  proxied = true
}

resource "cloudflare_record" "godaddy_paylink" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "pay.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "paylinks.commerce.godaddy.com"
  proxied = true
}

resource "cloudflare_record" "mailgun" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "track.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "mailgun.org"
  proxied = true
}

resource "cloudflare_record" "unbounce" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "try.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "4aeee6a9e5a245a09a937d23a15e7caf.unbouncepages.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "tutanota" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "speakup.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "login.tutanota.com"
  proxied = false
}

resource "cloudflare_record" "tutanota_domainkey_1" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "s1._domainkey.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "s1.domainkey.tutanota.de"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "tutanota_domainkey_2" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "s2._domainkey.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "s2.domainkey.tutanota.de"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "_mta_sts_tutanota" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_mta-sts.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "mta-sts.tutanota.de"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "mta_sts_tutanota" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "mta-sts.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "mta-sts.tutanota.de"
  proxied = false
  ttl     = 1
}

# MX Records

resource "cloudflare_record" "mail_tutanota" {
  zone_id  = cloudflare_zone.fluidattacks_tech.id
  name     = "@"
  type     = "MX"
  value    = "mail.tutanota.de"
  proxied  = false
  ttl      = 1
  priority = 10
}

# SRV Records

resource "cloudflare_record" "autodiscover" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_autodiscover._tcp"
  type    = "SRV"

  data {
    service  = "_autodiscover"
    proto    = "_tcp"
    name     = "autodiscover-srv.${cloudflare_zone.fluidattacks_tech.zone}"
    priority = 0
    weight   = 0
    port     = 443
    target   = "autodiscover.secureserver.net"
  }
}

# TXT Records

resource "cloudflare_record" "tutanota_verify" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "@"
  type    = "TXT"
  value   = "t-verify=441106cc5e96edbcba6574662f52aafd"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "spf_mail_tutanota" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "@"
  type    = "TXT"
  value   = "v=spf1 include:spf.tutanota.de -all"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "dmarc" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_dmarc.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "TXT"
  value   = "v=DMARC1; p=reject;"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "pic_domainkey" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "pic._domainkey"
  type    = "TXT"
  value   = "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDhlWESKfHJ7mhabvLjIC149sXmbq17kxA/Zivg57SkPtleeANMKK4WbAKl1WtQHnGqSoNsQ8WqoKCPqeSyrc4Sqjg6TJQi7mSq6tNR+gCALB6wSHRoAXwAoOcWkTJTyBUvzZjYaLk4bU7OlykNbYbN6BYudZ7mhIArimrXyttGzwIDAQAB"
  ttl     = 1
  proxied = false
}

resource "cloudflare_page_rule" "redirect_landing" {
  zone_id  = data.cloudflare_zone.fluidattacks_com.id
  target   = "landing.${data.cloudflare_zone.fluidattacks_com.name}/*"
  status   = "active"
  priority = 100

  actions {
    forwarding_url {
      url         = "https://try.${cloudflare_zone.fluidattacks_tech.zone}/$1"
      status_code = 301
    }
  }
}
