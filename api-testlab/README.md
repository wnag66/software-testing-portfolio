# Device and Order API Test Lab

The API lab is a Spring Boot service used to practice functional testing, API automation, database validation, defect reproduction, regression testing, and performance testing.

## Endpoints

| Method | Path | Expected behavior |
| --- | --- | --- |
| GET | `/api/v1/devices/{deviceId}/status` | Returns device state; unknown device is 404 |
| POST | `/api/v1/devices/{deviceId}/heartbeat` | Updates health data; invalid status or negative latency is 400 |
| POST | `/api/v1/orders/{orderId}/validate` | Accepts a valid order; rejects expired or repeated validation |
| GET | `/api/v1/events` | Supports type, severity, locationCode, page, and size filters |
| GET | `/actuator/health` | Returns service health |

## Run

```powershell
mvn -pl api-testlab spring-boot:run
```

Example:

```bash
curl http://localhost:8080/api/v1/devices/D001/status
curl "http://localhost:8080/api/v1/events?severity=HIGH&page=1&size=10"
```

## Test Assets

- Eight REST Assured regression tests with Allure annotations.
- Twenty manual cases in `docs/test-cases.md`.
- Five defect reports in `docs/bug-reports/`.
- Postman collection in `postman/device-order-api.postman_collection.json`.
- Parameterized JMeter plan in `jmeter/device-order-api.jmx`.

## Regression Command

```powershell
mvn -pl api-testlab test
```

The fixed release must run 8 tests with 0 failures.

