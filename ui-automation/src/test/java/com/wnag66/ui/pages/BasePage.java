package com.wnag66.ui.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public abstract class BasePage {

    protected final WebDriver driver;
    protected final WebDriverWait wait;

    protected BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(12));
    }

    protected WebElement visible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    protected WebElement clickable(By locator) {
        return wait.until(ExpectedConditions.elementToBeClickable(locator));
    }

    protected void click(By locator) {
        WebElement element = clickable(locator);
        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
    }

    protected void type(By locator, String value) {
        WebElement element = visible(locator);
        ((JavascriptExecutor) driver).executeScript("""
                const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
                setter.call(arguments[0], arguments[1]);
                arguments[0].dispatchEvent(new Event("input", { bubbles: true }));
                arguments[0].dispatchEvent(new Event("change", { bubbles: true }));
                """, element, value);
    }

    protected String text(By locator) {
        return visible(locator).getText();
    }

    protected void waitForUrl(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
    }
}
