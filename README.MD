
# SATSTOGO BACKEND
Please install the necessary packages before proceeding:

```
pip install -r requirements.txt
```

To run the project, use the command:

```
python3 manage.py runserver
```

To run database migrations:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Authentication APIs

The following flow is expected for the authentication APIs:

1. To Login a user, perform a GET request to the endpoint `api/auth-login/` with the param `k1`. A successful login reluts in the response: `{"status": "OK"}` while the opposite results: `{"status": "ERROR", "message": "Magic String Not Found"}`

2. To register a new user, make a GET API call to `api/auth/`. This endpoint responds with:
    ```json
    {"status": "OK","magic_string":hex_data,"auth_url":auth_url,"encoded":encoded}
    ```
    After you get this reponse, please open a websocket connection at `ws/notifications/{k1}/` where k1 is the magic string received.

3. When the user connects the LN wallet, you will receive a message on the websocket connnection in the form `{"status": "OK","message":"Verification Successful"}`

## Testing Websocket
This Javascript code snnippet can be used to test Websocket connections:
```javascript
const chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/654/');

chatSocket.onopen = function() {
  console.log('WebSocket connection established.');
  const message = {
    'message': 'Hello, world!'
  };
  chatSocket.send(JSON.stringify(message));
};
chatSocket.onmessage = function(event) {
  const message = JSON.parse(event.data);
  console.log('Received message:', message);
};
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
```

## RESOURCES
- https://github.com/lnurl/luds?tab=readme-ov-file#lnurl-documents