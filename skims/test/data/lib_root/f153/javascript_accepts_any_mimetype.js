// Following functions are expected to fail
// Lines 7, 20 and 38 should be marked

function mustFail1() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "https://jsonplaceholder.typicode.com/posts");
  xhr.setRequestHeader("Accept", "*/*");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log(xhr.responseText);
    }
  };
  xhr.send();
}

const mustFail2 = () => {
  const instance = new XMLHttpRequest();
  instance.open("POST", "https://jsonplaceholder.typicode.com/posts");
  instance.setRequestHeader("Content-Type", "application/json");
  instance.setRequestHeader("Accept", "*/*");
  instance.onreadystatechange = function () {
    if (instance.readyState === XMLHttpRequest.DONE) {
      console.log(instance.responseText);
    }
  };
  const data = JSON.stringify({
    title: "foo",
    body: "bar",
    userId: 1,
  });
  instance.send(data);
};

function mustFail3() {
  const example = new XMLHttpRequest();
  example.open("PUT", "https://jsonplaceholder.typicode.com/posts/1");
  example.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  example.setRequestHeader("Accept", "*/*");
  example.onreadystatechange = function () {
    if (example.readyState === XMLHttpRequest.DONE) {
      console.log(example.responseText);
    }
  };
  const data = new URLSearchParams();
  data.append("title", "foo");
  data.append("body", "bar");
  data.append("userId", "1");
  example.send(data);
}

function mustFail4() {
  const headers = new Headers();
  headers.append("Accept-Language", "en-US");
  headers.append("Accept", "*/*");
}

// Following functions are expected to pass
// No lines should be marked

function mustPass1() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "https://jsonplaceholder.typicode.com/posts");
  xhr.setRequestHeader("Accept", "any/*");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log(xhr.responseText);
    }
  };
  xhr.send();
}

const mustPass2 = () => {
  const instance = new XMLHttpRequest();
  instance.open("POST", "https://jsonplaceholder.typicode.com/posts");
  instance.setRequestHeader("Content-Type", "application/json");
  instance.onreadystatechange = function () {
    if (instance.readyState === XMLHttpRequest.DONE) {
      console.log(instance.responseText);
    }
  };
  const data = JSON.stringify({
    title: "foo",
    body: "bar",
    userId: 1,
  });
  xhr.send(data);
};

function mustFail3() {
  const example = new OtherClass();
  example.open("PUT", "https://jsonplaceholder.typicode.com/posts/1");
  example.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  example.setRequestHeader("Accept", "*/*");
  example.onreadystatechange = function () {
    if (example.readyState === XMLHttpRequest.DONE) {
      console.log(example.responseText);
    }
  };
  const data = new URLSearchParams();
  data.append("title", "foo");
  data.append("body", "bar");
  data.append("userId", "1");
  example.send(data);
}
