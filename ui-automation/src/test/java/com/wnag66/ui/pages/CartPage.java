package com.wnag66.ui.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;
import java.util.stream.Collectors;

public class CartPage extends BasePage {

    private static final By ITEM_NAMES = By.cssSelector("[data-test='inventory-item-name']");
    private static final By CHECKOUT = By.cssSelector("[data-test='checkout']");

    public CartPage(WebDriver driver) {
        super(driver);
    }

    public List<String> itemNames() {
        return driver.findElements(ITEM_NAMES).stream()
                .map(element -> element.getText())
                .collect(Collectors.toList());
    }

    public CheckoutPage checkout() {
        click(CHECKOUT);
        waitForUrl("checkout-step-one.html");
        return new CheckoutPage(driver);
    }
}

