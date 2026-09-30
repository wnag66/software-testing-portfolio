# Software Testing Portfolio

[![CI](https://github.com/wnag66/software-testing-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/wnag66/software-testing-portfolio/actions/workflows/ci.yml)

这是一个面向通用软件测试实习岗位的个人测试实践仓库。项目包含 API 功能与性能测试、SauceDemo Web UI 自动化测试、缺陷复现与回归、Allure 报告以及 GitHub Actions 持续集成。

仓库中的被测系统是自建 API 靶场，缺陷版本用于演示发现、复现、修复和回归过程，不代表任何企业的真实生产系统。

## Results

| Project | Scope | Execution | Result |
| --- | --- | --- | --- |
| Device and Order API | 4 API, 20 manual cases, 8 automated tests | REST Assured + JUnit 5 | 8/8 passed |
| SauceDemo UI | Login, sorting, cart, checkout, logout | Selenium + JUnit 5 + POM | 10/10 passed |
| Defect lifecycle | 5 defects in API behavior | v0.1-buggy -> v1.0-fixed | 5/5 reproduced, 5/5 regressed |
| Performance | Smoke, 20-user baseline, 50-user load | JMeter 5.6.3 | 0% error rate in all scenarios |

Performance results were collected on a local single-node Spring Boot and H2 test lab. They demonstrate JMeter workflow and result analysis, not production capacity.

## Repository Layout

```text
api-testlab/       Spring Boot API laboratory and REST Assured tests
ui-automation/     Selenium Page Object automation for SauceDemo
postman/           Postman collection for API exploration
docs/              test plan, manual cases, defect reports, evidence
reports/           generated Allure HTML reports
scripts/           PDF generation script
```

## Run Locally

API regression:

```powershell
mvn -pl api-testlab test
```

UI automation:

```powershell
mvn -pl ui-automation test "-Dheadless=true" `
  "-Dwebdriver.chrome.driver=C:\path\to\chromedriver.exe"
```

Performance scenarios:

```powershell
.\api-testlab\scripts\run-performance.ps1
```

The JMeter script runs smoke, baseline, and load scenarios, then writes HTML dashboards and raw results under `api-testlab/jmeter/reports/`. That generated directory is excluded from Git because raw JTL files are large.

## Defect Version

`v0.1-buggy` contains five intentionally preserved defects. `v1.0-fixed` contains the fixes and a passing regression suite. The failure evidence is recorded in `docs/evidence/buggy-test-run.md`.

## Reports

- API Allure: `reports/allure-api/index.html`
- UI Allure: `reports/allure-ui/index.html`
- API test plan: `docs/test-plan.md`
- Manual cases: `docs/test-cases.md`
- Performance summary: `docs/performance-results.md`

