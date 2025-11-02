Invoke-RestMethod -Uri "http://localhost:7000/agent" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"query": "Add 5 and 3, then find gcd of that result with 4"}'