module "github_makes" {
  source = "./modules/github"

  description = "A software supply chain framework powered by Nix."
  homepage    = "https://makes.fluidattacks.com/"
  name        = "makes"
  token       = var.githubToken
  topics      = ["build", "cd", "ci", "devops", "devsecops", "nix"]

  secrets = {}

  pages = {
    cname = "makes.fluidattacks.com"
  }
}
