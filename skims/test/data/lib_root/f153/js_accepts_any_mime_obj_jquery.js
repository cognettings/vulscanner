const dangHeaders = {
  Accept: "*/*",
};

function jQueryMustFail() {
  $.ajax({
    url: "https://example.com/api",
    method: "GET",
    headers: {
      Authorization: "Bearer YOUR_ACCESS_TOKEN_HERE",
      Accept: "*/*",
    },
    success: function (data) {
      console.log(data);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function jQueryMustFailII() {
  $.ajax({
    url: "https://example.com/api",
    method: "GET",
    headers: dangHeaders,
    success: function (data) {
      console.log(data);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function mustPass() {
  $.ajax({
    url: "https://example.com/api",
    method: "GET",
    headers: {
      Authorization: "Bearer YOUR_ACCESS_TOKEN_HERE",
    },
    success: function (data) {
      console.log(data);
    },
    error: function (error) {
      console.log(error);
    },
  });
}
