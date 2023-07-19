import axios from 'axios';


const dangHeadersI = new Headers({
  'Content-Type': 'application/json',
  'Authorization': 'Bearer <token>',
  'X-Custom-Header': 'custom value',
  'Accept': '*/*',
  'Cache-Control': 'no-cache'
});

const dangHeadersII = {
  Accept: '*/*'
};

const axiosMustFail = () => {
  axios.get('https://example.com', {
    headers: dangHeadersI
  })
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
};

const fetchMustFail = () => {
  fetch('https://example.com', {
    headers: new Headers(dangHeadersII)
  })
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error(error));
};
