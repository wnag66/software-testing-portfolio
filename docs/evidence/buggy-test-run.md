# Buggy Version Evidence

Command:

```text
mvn -pl api-testlab test
```

Result before fixes:

```text
Tests run: 8, Failures: 5, Errors: 0, Skipped: 0
```

Observed failures:

| Test | Actual | Expected |
| --- | --- | --- |
| Negative heartbeat latency | 200 | 400 |
| Expiry boundary | accepted=true | accepted=false |
| Duplicate validation | second request 200 | 409 |
| Zero page size | 500 | 400 |
| Oversized page size | 200 | 400 |

This run is the baseline for BUG-001 through BUG-005.

