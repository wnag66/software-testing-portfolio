package com.wnag66.ui.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;

public class InventoryPage extends BasePage {

    private static final By TITLE = By.cssSelector("[data-test='title']");
    private static final By SORT = By.cssSelector("[data-test='product-sort-container']");
    private static final By PRODUCT_NAMES = By.cssSelector(".inventory_item_name");
    private static final By CART_LINK = By.cssSelector("[data-test='shopping-cart-link']");
    private static final By CART_BADGE = By.cssSelector("[data-test='shopping-cart-badge']");
    private static final By MENU_BUTTON = By.id("react-burger-menu-btn");
    private static final By LOGOUT_LINK = By.id("logout_sidebar_link");
    private static final By BACKPACK_ADD = By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']");
    private static final By BACKPACK_REMOVE = By.cssSelector("[data-test='remove-sauce-labs-backpack']");

    public InventoryPage(WebDriver driver) {
        super(driver);
    }

    public boolean isLoaded() {
        return "Products".equals(text(TITLE));
    }

    public InventoryPage waitUntilReady() {
        visible(TITLE);
        wait.until(webDriver ->
                Boolean.TRUE.equals(((JavascriptExecutor) webDriver).executeScript("""
                        const element = document.querySelector("[data-test='add-to-cart-sauce-labs-backpack']");
                        return element && Object.keys(element).some(key => key.startsWith("__reactProps$"));
                        """))
        );
        wait.until(webDriver ->
                Boolean.TRUE.equals(((JavascriptExecutor) webDriver).executeScript("""
                        const element = document.querySelector("#react-burger-menu-btn");
                        return element && Object.keys(element).some(key => key.startsWith("__reactProps$"));
                        """))
        );
        return this;
    }

    public InventoryPage sortBy(String value) {
        org.openqa.selenium.support.ui.Select select =
                new org.openqa.selenium.support.ui.Select(visible(SORT));
        select.selectByValue(value);
        return this;
    }

    public String firstProductName() {
        return text(SORT);
    }

    public String firstProductText() {
        return driver.findElements(PRODUCT_NAMES).get(0).getText();
    }

    public InventoryPage addBackpackToCart() {
        click(BACKPACK_ADD);
        wait.until(ExpectedConditions.visibilityOfElementLocated(CART_BADGE));
        return this;
    }

    public InventoryPage removeBackpackFromCart() {
        click(BACKPACK_REMOVE);
        wait.until(ExpectedConditions.invisibilityOfElementLocated(CART_BADGE));
        return this;
    }

    public String cartBadgeText() {
        return text(CART_BADGE);
    }

    public CartPage openCart() {
        click(CART_LINK);
        waitForUrl("cart.html");
        return new CartPage(driver);
    }

    public LoginPage logout() {
        click(MENU_BUTTON);
        click(LOGOUT_LINK);
        waitForUrl("saucedemo.com");
        return new LoginPage(driver);
    }
}
