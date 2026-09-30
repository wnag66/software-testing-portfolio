# Manual Test Cases

| ID | Module | Scenario | Expected Result | Automated |
| --- | --- | --- | --- | --- |
| TC-API-001 | Device | Query existing device D001 | 200 and correct device/location/status fields | Yes |
| TC-API-002 | Device | Query unknown device D999 | 404 NOT_FOUND | Yes |
| TC-API-003 | Device | Query malformed device ID | 400 INVALID_REQUEST | No |
| TC-API-004 | Heartbeat | Submit valid ONLINE heartbeat | 200 and updated latency | No |
| TC-API-005 | Heartbeat | Submit unsupported status | 400 INVALID_REQUEST | No |
| TC-API-006 | Heartbeat | Submit negative latency | 400 and state remains unchanged | Yes |
| TC-API-007 | Order | Validate a valid order | 200 accepted=true | Yes |
| TC-API-008 | Order | Validate an expired order | 200 accepted=false reason=EXPIRED | No |
| TC-API-009 | Order | Validate exactly at the expiry timestamp | Reject as expired | Yes |
| TC-API-010 | Order | Validate the same order twice | First 200, second 409 DUPLICATE_REQUEST | Yes |
| TC-API-011 | Order | Validate a missing order | 404 NOT_FOUND | No |
| TC-API-012 | Order | Validate with an invalid location code | 400 INVALID_REQUEST | No |
| TC-API-013 | Event | Query the first page with size 10 | 200 and at most 10 items | No |
| TC-API-014 | Event | Filter by HIGH severity | Only HIGH events are returned | No |
| TC-API-015 | Event | Filter by type and location | Results satisfy both filters | No |
| TC-API-016 | Event | Request page 0 | 400 INVALID_REQUEST | No |
| TC-API-017 | Event | Request size 0 | 400 INVALID_REQUEST | Yes |
| TC-API-018 | Event | Request size 51 | 400 INVALID_REQUEST | Yes |
| TC-API-019 | Event | Request maximum size 50 | 200 and exactly 50 items | Yes |
| TC-API-020 | Event | Verify database count matches pagination total | API total equals SQL count | No |

