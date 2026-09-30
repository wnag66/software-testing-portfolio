# SauceDemo UI Automation

This module automates the public SauceDemo demonstration site with Selenium, Java, JUnit 5, Allure, and the Page Object Model.

## Coverage

The suite contains 10 cases:

- Standard login
- Locked user
- Invalid password
- Product sorting
- Add to cart
- Remove from cart
- Cart content
- Checkout completion
- Required-field validation
- Logout

The tests use explicit waits and stable `data-test` selectors. A failure watcher attaches a screenshot and page source to the Allure result.

## Run

```powershell
mvn -pl ui-automation test "-Dheadless=true" `
  "-Dwebdriver.chrome.driver=C:\path\to\chromedriver.exe"
```

Set `-Dheadless=false` to watch the browser locally.

## Known Constraints

- SauceDemo is an external demonstration site, so network availability is required.
- The local Chrome major version must match the downloaded ChromeDriver major version.
- CI pins Chrome and ChromeDriver to the same version.

