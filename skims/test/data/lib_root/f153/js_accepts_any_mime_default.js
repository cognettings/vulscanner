const axiosAlias = require("axios");

// Gloabal axios default
// Line 9 must fail.
axiosAlias.defaults.baseURL = "https://api.example.com";
axiosAlias.defaults.headers.common["Authorization"] = AUTH_TOKEN;
axiosAlias.defaults.headers.post["Content-Type"] =
  "application/x-www-form-urlencoded";
axiosAlias.defaults.headers.post["Accept"] = "*/*";

const instance = axiosAlias.create({
  baseURL: "https://api.example.com",
});

let dang_value = "*/*";
// Alter defaults after instance has been created
instance.defaults.headers.common["Authorization"] = AUTH_TOKEN;
instance.defaults.headers.common["Accept"] = dang_value;
