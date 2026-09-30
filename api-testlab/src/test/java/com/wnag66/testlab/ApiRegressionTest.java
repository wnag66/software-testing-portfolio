package com.wnag66.testlab;

import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Severity;
import io.qameta.allure.SeverityLevel;
import io.qameta.allure.Story;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.jdbc.Sql;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.hasSize;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@Sql(scripts = "/reset.sql", executionPhase = Sql.ExecutionPhase.BEFORE_TEST_METHOD)
@Epic("Device and Order API")
@Feature("API regression")
class ApiRegressionTest {

    @LocalServerPort
    private int port;

    @BeforeEach
    void configureRestAssured() {
        RestAssured.port = port;
        RestAssured.basePath = "";
    }

    @Test
    @Story("Device status")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-API-001 device status returns expected schema")
    void deviceStatusReturnsExpectedSchema() {
        given()
                .accept(ContentType.JSON)
                .when()
                .get("/api/v1/devices/D001/status")
                .then()
                .statusCode(200)
                .body("deviceId", equalTo("D001"))
                .body("locationCode", equalTo("L001"))
                .body("status", equalTo("ONLINE"))
                .body("latencyMs", greaterThanOrEqualTo(0));
    }

    @Test
    @Story("Device status")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-API-002 unknown device returns 404")
    void unknownDeviceReturns404() {
        given()
                .accept(ContentType.JSON)
                .when()
                .get("/api/v1/devices/D999/status")
                .then()
                .statusCode(404)
                .body("code", equalTo("NOT_FOUND"));
    }

    @Test
    @Story("Heartbeat")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-API-003 negative heartbeat latency is rejected")
    void negativeHeartbeatLatencyIsRejected() {
        given()
                .contentType(ContentType.JSON)
                .body("""
                        {
                          "status": "ONLINE",
                          "timestamp": "2026-09-30T10:00:00Z",
                          "latencyMs": -1
                        }
                        """)
                .when()
                .post("/api/v1/devices/D001/heartbeat")
                .then()
                .statusCode(400)
                .body("code", equalTo("INVALID_REQUEST"));
    }

    @Test
    @Story("Order validation")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-API-004 valid order is accepted")
    void validOrderIsAccepted() {
        given()
                .contentType(ContentType.JSON)
                .body("""
                        {
                          "locationCode": "L001",
                          "gateId": "G001",
                          "validatedAt": "2026-09-30T10:00:00Z"
                        }
                        """)
                .when()
                .post("/api/v1/orders/O1001/validate")
                .then()
                .statusCode(200)
                .body("accepted", equalTo(true))
                .body("reason", equalTo("VALID"));
    }

    @Test
    @Story("Order validation")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-API-005 expiry boundary is treated as expired")
    void expiryBoundaryIsTreatedAsExpired() {
        given()
                .contentType(ContentType.JSON)
                .body("""
                        {
                          "locationCode": "L001",
                          "gateId": "G001",
                          "validatedAt": "2099-12-31T15:59:59Z"
                        }
                        """)
                .when()
                .post("/api/v1/orders/O1001/validate")
                .then()
                .statusCode(200)
                .body("accepted", equalTo(false))
                .body("reason", equalTo("EXPIRED"));
    }

    @Test
    @Story("Order validation")
    @Severity(SeverityLevel.CRITICAL)
    @DisplayName("TC-API-006 duplicate validation is rejected")
    void duplicateValidationIsRejected() {
        String request = """
                {
                  "locationCode": "L001",
                  "gateId": "G001",
                  "validatedAt": "2026-09-30T10:00:00Z"
                }
                """;

        given()
                .contentType(ContentType.JSON)
                .body(request)
                .when()
                .post("/api/v1/orders/O1001/validate")
                .then()
                .statusCode(200);

        given()
                .contentType(ContentType.JSON)
                .body(request)
                .when()
                .post("/api/v1/orders/O1001/validate")
                .then()
                .statusCode(409)
                .body("code", equalTo("DUPLICATE_REQUEST"));
    }

    @Test
    @Story("Event pagination")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-API-007 zero page size is rejected")
    void zeroPageSizeIsRejected() {
        given()
                .accept(ContentType.JSON)
                .queryParam("page", 1)
                .queryParam("size", 0)
                .when()
                .get("/api/v1/events")
                .then()
                .statusCode(400)
                .body("code", equalTo("INVALID_REQUEST"));
    }

    @Test
    @Story("Event pagination")
    @Severity(SeverityLevel.NORMAL)
    @DisplayName("TC-API-008 oversized page size is rejected")
    void oversizedPageSizeIsRejected() {
        given()
                .accept(ContentType.JSON)
                .queryParam("page", 1)
                .queryParam("size", 51)
                .when()
                .get("/api/v1/events")
                .then()
                .statusCode(400)
                .body("code", equalTo("INVALID_REQUEST"));

        given()
                .accept(ContentType.JSON)
                .queryParam("page", 1)
                .queryParam("size", 50)
                .when()
                .get("/api/v1/events")
                .then()
                .statusCode(200)
                .body("items", hasSize(50));
    }
}

