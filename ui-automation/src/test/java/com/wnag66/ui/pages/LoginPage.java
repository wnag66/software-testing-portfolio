package com.wnag66.ui.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;

public class LoginPage extends BasePage {

    private static final By USERNAME = By.cssSelector("[data-test='username']");
    private static final By PASSWORD = By.cssSelector("[data-test='password']");
    private static final By LOGIN_BUTTON = By.cssSelector("[data-test='login-button']");
    private static final By ERROR = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage open() {
        driver.get("https://www.saucedemo.com/");
        visible(LOGIN_BUTTON);
        return this;
    }

    public InventoryPage loginAs(String username, String password) {
        type(USERNAME, username);
        type(PASSWORD, password);
        submitForm();
        waitForUrl("inventory.html");
        return new InventoryPage(driver).waitUntilReady();
    }

    public LoginPage submitInvalidCredentials(String username, String password) {
        type(USERNAME, username);
        type(PASSWORD, password);
        submitForm();
        visible(ERROR);
        return this;
    }

    public String errorMessage() {
        return text(ERROR);
    }

    private void submitForm() {
        ((JavascriptExecutor) driver).executeScript(
                "document.querySelector('form[aria-label=\"Login\"]').requestSubmit();"
        );
    }
}
