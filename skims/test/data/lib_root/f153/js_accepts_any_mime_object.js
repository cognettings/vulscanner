const axiosAlias = require("axios");

const dangHeaders = {
  Accept: "*/*",
};

function axiosMustFail() {
  axiosAlias
    .get("https://example.com", {
      headers: dangHeaders,
    })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function fetchMustFail() {
  fetch("https://example.com", {
    headers: new Headers(dangHeaders),
  })
    .then((response) => response.text())
    .then((data) => console.log(data))
    .catch((error) => console.error(error));
}

function axiosMustFail() {
  axiosAlias
    .get("https://example.com", {
      headers: {
        Connection: "keep-alive",
        Accept: "*/*",
      },
    })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function kyMustFail() {
  const ky = require("ky");

  ky("https://jsonplaceholder.typicode.com/posts", {
    headers: {
      Authorization: "Bearer my-token",
      Accept: "*/*",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      console.log(response.json());
    })
    .catch((error) => {
      console.error(error);
    });
}

function mustPass() {
  axiosAlias
    .get("https://example.com", {
      headers: {
        Connection: "keep-alive",
        Accept: "text/html",
      },
    })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function kyMustPass() {
  const ky = require("ky");

  ky("https://jsonplaceholder.typicode.com/posts", {
    headers: {
      Authorization: "Bearer my-token",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      console.log(response.json());
    })
    .catch((error) => {
      console.error(error);
    });
}
