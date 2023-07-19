resource "azurerm_storage_account" "example" {
  name                     = "storageaccountname"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  min_tls_version          = "TLS1_0"

  tags = {
    environment = "staging"
  }
}
resource "azapi_resource" "unsafe_api" {
  name = "storageaccountname"
  properties = {
    siteConfig = {
      minTlsVersion            = "1.0"
      dotnet_framework_version = "v4.0"
    }
  }
}

resource "azapi_resource" "safe_api" {
  name = "storageaccountname"
  properties = {
    site_name = "myexample"
    siteConfig = {
      dotnet_framework_version = "v4.0"
      minTlsVersion            = "1.2"
    }
  }
}
