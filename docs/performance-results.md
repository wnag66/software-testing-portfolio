# API Performance Results

## Environment

- Test date: 2026-09-30
- JMeter: 5.6.3
- Java: 17.0.20
- Application: local Spring Boot 3.5.16 single node
- Database: in-memory H2
- Endpoint mix: health, device status, heartbeat, event query

These results describe a local demonstration environment. They must not be presented as production capacity.

## Scenario Summary

| Scenario | Concurrency | Ramp-up | Duration | Samples | Throughput | Average | P90 | P95 | Error Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Smoke | 1 | 1 s | 10 s | 5,083 | 515.2 req/s | 1.81 ms | 4 ms | 4 ms | 0.00% |
| Baseline | 20 | 10 s | 60 s | 235,271 | 3,927.7 req/s | 4.62 ms | 20 ms | 23 ms | 0.00% |
| Load | 50 | 20 s | 120 s | 396,024 | 3,303.0 req/s | 13.83 ms | 56 ms | 70 ms | 0.00% |

## Endpoint Results Under 50 Users

| Endpoint | Samples | Throughput | Average | P90 | P95 | P99 | Errors |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Health | 99,039 | 826.0 req/s | 48.69 ms | 83 ms | 95 ms | 123 ms | 0 |
| Device status | 98,997 | 826.1 req/s | 1.63 ms | 3 ms | 7 ms | 19 ms | 0 |
| Heartbeat | 98,995 | 826.1 req/s | 2.71 ms | 8 ms | 15 ms | 29 ms | 0 |
| Event query | 98,993 | 826.0 req/s | 2.27 ms | 6 ms | 12 ms | 25 ms | 0 |

## Observations

- The service remained stable at 50 active users with no HTTP errors.
- Health endpoint latency increased more than business endpoints because of endpoint and actuator instrumentation overhead.
- Increasing from 20 to 50 users reduced total throughput from 3,927.7 to 3,303.0 req/s, indicating resource contention on the local machine.
- Longer-duration soak testing, JVM profiling, and database tuning are appropriate next steps.

