package com.wnag66.ui.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CheckoutPage extends BasePage {

    private static final By FIRST_NAME = By.cssSelector("[data-test='firstName']");
    private static final By LAST_NAME = By.cssSelector("[data-test='lastName']");
    private static final By POSTAL_CODE = By.cssSelector("[data-test='postalCode']");
    private static final By CONTINUE = By.cssSelector("[data-test='continue']");
    private static final By FINISH = By.cssSelector("[data-test='finish']");
    private static final By COMPLETE_HEADER = By.cssSelector("[data-test='complete-header']");
    private static final By ERROR = By.cssSelector("[data-test='error']");

    public CheckoutPage(WebDriver driver) {
        super(driver);
    }

    public CheckoutPage fillCustomerDetails(String firstName, String lastName, String postalCode) {
        if (!firstName.isEmpty()) {
            type(FIRST_NAME, firstName);
        }
        if (!lastName.isEmpty()) {
            type(LAST_NAME, lastName);
        }
        if (!postalCode.isEmpty()) {
            type(POSTAL_CODE, postalCode);
        }
        return this;
    }

    public CheckoutPage continueCheckout() {
        click(CONTINUE);
        return this;
    }

    public CheckoutPage finishOrder() {
        click(FINISH);
        waitForUrl("checkout-complete.html");
        return this;
    }

    public String completionMessage() {
        return text(COMPLETE_HEADER);
    }

    public String errorMessage() {
        return text(ERROR);
    }
}

