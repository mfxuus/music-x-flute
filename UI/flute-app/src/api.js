import config from './config.js';

export const serverWS = new WebSocket(config.websocketUrl);
const apiCall = {
  path: "dummy_path",
  data: { channel: "Hi!" },
};

serverWS.onopen = (event) => {
  serverWS.send(JSON.stringify(apiCall));
};

serverWS.onmessage = function (event) {
  console.log(event);
  const json = JSON.parse(event.data);
  console.log(json);
};

export const sendWsMsg = (msg) => {
  serverWS.send(JSON.stringify(msg));
}

