package com.wnag66.testlab.dto;

import java.time.Instant;

public record EventResponse(
        long eventId,
        String eventType,
        String severity,
        String locationCode,
        Instant occurredAt,
        String message
) {
}

