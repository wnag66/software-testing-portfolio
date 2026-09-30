# Software Test Plan

## Objective

Verify the functional behavior, input validation, data consistency, regression stability, and baseline performance of two independent software systems:

1. Device and Order API test lab.
2. SauceDemo demonstration web application.

The plan is designed to demonstrate an end-to-end testing workflow rather than production certification.

## Scope

### In Scope

- Device status query and heartbeat update.
- Order validation, expiry boundaries, and duplicate submission.
- Event filtering and pagination boundaries.
- Login, product sorting, cart operations, checkout, validation messages, and logout.
- REST Assured and Selenium regression suites.
- JMeter smoke, baseline, and load scenarios for the API lab.
- Defect reporting, regression, and release notes.

### Out of Scope

- Security penetration testing.
- Production capacity certification.
- Cross-browser matrix beyond current Chrome.
- Load testing against the external SauceDemo site.

## Test Strategy

| Layer | Approach | Tools |
| --- | --- | --- |
| Functional API | Positive, negative, boundary, and data consistency tests | Postman, JUnit 5, REST Assured |
| UI | User-journey automation with explicit waits and Page Object Model | Selenium, JUnit 5, Allure |
| Performance | Smoke, baseline, and load scenarios on a local single node | JMeter 5.6.3 |
| Defect management | Reproduce on `v0.1-buggy`, fix, and regress on `v1.0-fixed` | Git, Markdown, GitHub Issues |
| CI | Run API and UI suites on each push | GitHub Actions |

## Test Cases

The manual suite contains 20 cases in `docs/test-cases.md`. The automated API suite contains 8 cases. The UI suite contains 10 cases.

## Entry Criteria

- Java 17 and Maven 3.9+ are available.
- API application starts with an in-memory H2 database.
- Chrome and a matching ChromeDriver are available for UI tests.
- SauceDemo is reachable from the test environment.

## Exit Criteria

- API regression: 8/8 passed.
- UI regression: 10/10 passed.
- All five known defects are reproduced on the buggy version and closed on the fixed version.
- No critical or high-severity open defect remains.
- Allure reports are generated successfully.
- JMeter scenarios complete with recorded throughput, latency, and error rate.

## Risk

- SauceDemo is external and can change without notice.
- Local performance results are affected by the machine, JVM warm-up, H2 storage, and background load.
- Automated UI tests are limited to one browser engine.

