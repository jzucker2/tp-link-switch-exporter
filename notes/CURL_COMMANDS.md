# Curl Commands

```
curl -i "http://localhost:3133/api/v1/tp-link-switch/test" \
-H "Content-Type: application/json"

# check on a device
curl -i "http://10.0.1.8:3133/api/v1/tp-link-switch/test" \
    -H "Content-Type: application/json"
```

## Dev

```
curl -i "http://10.0.1.8:3133/api/v1/debug" \
-H "Content-Type: application/json"

curl -i "http://10.0.1.8:3133/api/v1/collector/simple" \
-H "Content-Type: application/json"

curl -i "http://10.0.1.8:3133/api/v1/collector/metrics/update" \
-H "Content-Type: application/json"
```
