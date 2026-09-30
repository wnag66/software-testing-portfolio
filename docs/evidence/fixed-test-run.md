# Fixed Version Evidence

## API Regression

Command:

```text
mvn -pl api-testlab test
```

Result:

```text
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

## Combined Maven Verification

Command:

```text
mvn clean verify -Dheadless=true -Dwebdriver.chrome.driver=<matching-driver>
```

Result:

```text
Software Testing Portfolio ... SUCCESS
Device and Order API Test Lab ... SUCCESS
SauceDemo UI Automation ... SUCCESS
BUILD SUCCESS
```

## UI Regression

Command:

```text
mvn -pl ui-automation test -Dheadless=true -Dwebdriver.chrome.driver=<matching-driver>
```

Result:

```text
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```
