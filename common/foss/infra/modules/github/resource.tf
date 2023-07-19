resource "github_actions_secret" "secrets" {
  for_each        = var.secrets
  repository      = github_repository.repo.name
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_branch_default" "default" {
  repository = github_repository.repo.name
  branch     = "main"
}

resource "github_branch_protection" "main" {
  allows_force_pushes             = false
  allows_deletions                = false
  enforce_admins                  = true
  pattern                         = "main"
  repository_id                   = github_repository.repo.node_id
  require_conversation_resolution = true
  require_signed_commits          = false

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    required_approving_review_count = 1
  }

  required_status_checks {
    strict   = false
    contexts = []
  }
}

resource "github_repository" "repo" {
  allow_merge_commit     = true
  allow_squash_merge     = false
  allow_rebase_merge     = false
  auto_init              = true
  delete_branch_on_merge = false
  description            = var.description
  has_downloads          = false
  has_issues             = true
  has_projects           = true
  has_wiki               = false
  homepage_url           = var.homepage
  is_template            = false
  license_template       = "mit"
  name                   = var.name
  topics                 = var.topics
  vulnerability_alerts   = false
  visibility             = "public"

  dynamic "pages" {
    for_each = var.pages != {} ? [1] : []
    content {
      cname = var.pages.cname
      source {
        branch = "gh-pages"
        path   = "/"
      }
    }
  }

}
