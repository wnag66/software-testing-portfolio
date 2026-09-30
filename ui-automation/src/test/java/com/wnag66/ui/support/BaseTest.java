package com.wnag66.ui.support;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

@ExtendWith(ScreenshotOnFailure.class)
public abstract class BaseTest {

    protected static final String BASE_URL = "https://www.saucedemo.com/";

    protected static WebDriver driver;

    @BeforeAll
    static void startBrowser() {
        DriverFactory.start();
        driver = DriverFactory.get();
    }

    @BeforeEach
    void resetSession() {
        navigateToEntryPage();
        driver.manage().deleteAllCookies();
        ((JavascriptExecutor) driver).executeScript("window.localStorage.clear(); window.sessionStorage.clear();");
        navigateToEntryPage();
        new WebDriverWait(driver, Duration.ofSeconds(20))
                .until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("[data-test='login-button']")));
    }

    private void navigateToEntryPage() {
        try {
            driver.get(BASE_URL);
        } catch (TimeoutException exception) {
            ((JavascriptExecutor) driver).executeScript("window.stop();");
        }
        new WebDriverWait(driver, Duration.ofSeconds(30)).until(webDriver ->
                "complete".equals(((JavascriptExecutor) webDriver).executeScript("return document.readyState"))
        );
    }

    @AfterAll
    static void stopBrowser() {
        DriverFactory.quit();
    }
}
