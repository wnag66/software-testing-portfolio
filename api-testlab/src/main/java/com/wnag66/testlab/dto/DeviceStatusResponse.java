package com.wnag66.testlab.dto;

import java.time.Instant;

public record DeviceStatusResponse(
        String deviceId,
        String deviceName,
        String locationCode,
        String status,
        Instant lastHeartbeat,
        int latencyMs
) {
}

