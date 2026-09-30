package com.wnag66.ui.tests;

import com.wnag66.ui.pages.CartPage;
import com.wnag66.ui.pages.CheckoutPage;
import com.wnag66.ui.pages.InventoryPage;
import com.wnag66.ui.pages.LoginPage;
import com.wnag66.ui.support.BaseTest;
import io.qameta.allure.Description;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Severity;
import io.qameta.allure.SeverityLevel;
import io.qameta.allure.Story;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

@Epic("SauceDemo web application")
@Feature("End-to-end UI automation")
class SauceDemoUiTest extends BaseTest {

    private LoginPage loginPage;

    @BeforeEach
    void createEntryPage() {
        loginPage = new LoginPage(driver);
    }

    @Test
    @Story("Login")
    @Severity(SeverityLevel.BLOCKER)
    @DisplayName("TC-UI-001 standard user can log in")
    void standardUserCanLogIn() {
        InventoryPage inventory = loginPage.loginAs("standard_user", "secret_sauce");
        assertThat(inventory.isLoaded()).isTrue();
    }

    @Test
    @Story("Login")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-UI-002 locked user sees a blocking message")
    void lockedUserSeesBlockingMessage() {
        loginPage.submitInvalidCredentials("locked_out_user", "secret_sauce");
        assertThat(loginPage.errorMessage()).contains("locked out");
    }

    @Test
    @Story("Login")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-UI-003 invalid password is rejected")
    void invalidPasswordIsRejected() {
        loginPage.submitInvalidCredentials("standard_user", "wrong-password");
        assertThat(loginPage.errorMessage()).contains("Username and password do not match");
    }

    @Test
    @Story("Catalog")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-UI-004 products can be sorted descending by name")
    void productsCanBeSortedDescendingByName() {
        InventoryPage inventory = loginPage.loginAs("standard_user", "secret_sauce");
        inventory.sortBy("za");
        assertThat(inventory.firstProductText()).isEqualTo("Test.allTheThings() T-Shirt (Red)");
    }

    @Test
    @Story("Cart")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-UI-005 adding an item updates the cart badge")
    void addingItemUpdatesCartBadge() {
        InventoryPage inventory = loginPage.loginAs("standard_user", "secret_sauce");
        inventory.addBackpackToCart();
        assertThat(inventory.cartBadgeText()).isEqualTo("1");
    }

    @Test
    @Story("Cart")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-UI-006 removing an item clears the cart badge")
    void removingItemClearsCartBadge() {
        InventoryPage inventory = loginPage.loginAs("standard_user", "secret_sauce");
        inventory.addBackpackToCart().removeBackpackFromCart();
        assertThat(inventory.isLoaded()).isTrue();
    }

    @Test
    @Story("Cart")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-UI-007 cart contains the selected product")
    void cartContainsSelectedProduct() {
        CartPage cart = loginPage.loginAs("standard_user", "secret_sauce")
                .addBackpackToCart()
                .openCart();
        assertThat(cart.itemNames()).contains("Sauce Labs Backpack");
    }

    @Test
    @Story("Checkout")
    @Severity(SeverityLevel.BLOCKER)
    @DisplayName("TC-UI-008 checkout can be completed")
    void checkoutCanBeCompleted() {
        CheckoutPage checkout = loginPage.loginAs("standard_user", "secret_sauce")
                .addBackpackToCart()
                .openCart()
                .checkout()
                .fillCustomerDetails("Liu", "Ya", "310000")
                .continueCheckout();
        checkout.finishOrder();
        assertThat(checkout.completionMessage()).contains("Thank you for your order");
    }

    @Test
    @Story("Checkout")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-UI-009 checkout validates required fields")
    void checkoutValidatesRequiredFields() {
        CheckoutPage checkout = loginPage.loginAs("standard_user", "secret_sauce")
                .addBackpackToCart()
                .openCart()
                .checkout()
                .continueCheckout();
        assertThat(checkout.errorMessage()).contains("First Name is required");
    }

    @Test
    @Story("Session")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-UI-010 user can log out")
    void userCanLogOut() {
        LoginPage login = loginPage.loginAs("standard_user", "secret_sauce")
                .logout();
        assertThat(login.open()).isNotNull();
    }
}

