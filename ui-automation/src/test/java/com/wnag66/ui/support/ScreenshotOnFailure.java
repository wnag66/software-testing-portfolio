package com.wnag66.ui.support;

import io.qameta.allure.Allure;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.TestWatcher;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;

public class ScreenshotOnFailure implements TestWatcher {

    @Override
    public void testFailed(ExtensionContext context, Throwable cause) {
        WebDriver driver = DriverFactory.peek();
        if (driver == null) {
            return;
        }
        try {
            byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            Allure.addAttachment(
                    "Failure screenshot - " + context.getDisplayName(),
                    "image/png",
                    new ByteArrayInputStream(screenshot),
                    "png"
            );
            Allure.addAttachment(
                    "Page source - " + context.getDisplayName(),
                    "text/html",
                    new ByteArrayInputStream(driver.getPageSource().getBytes(StandardCharsets.UTF_8)),
                    "html"
            );
        } catch (RuntimeException ignored) {
            // Preserve the original test failure when the browser has already closed.
        }
    }
}

