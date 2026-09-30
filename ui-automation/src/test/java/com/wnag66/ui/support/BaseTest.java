package com.wnag66.ui.support;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.WebDriver;

@ExtendWith(ScreenshotOnFailure.class)
public abstract class BaseTest {

    protected static final String BASE_URL = "https://www.saucedemo.com/";

    protected WebDriver driver;

    @BeforeEach
    void startBrowser() {
        DriverFactory.start();
        driver = DriverFactory.get();
        driver.get(BASE_URL);
    }

    @AfterEach
    void stopBrowser() {
        DriverFactory.quit();
    }
}

