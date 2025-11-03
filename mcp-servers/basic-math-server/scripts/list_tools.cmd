set sessionId=

curl -X POST "http://127.0.0.1:8000/mcp" ^
-H "Content-Type: application/json" ^
-H "Accept: application/json, text/event-stream" ^
-H "Mcp-Session-Id: %sessionId%" ^
-d "{ \"jsonrpc\": \"2.0\", \"id\": 2, \"method\": \"tools/list\", \"params\": {} }"