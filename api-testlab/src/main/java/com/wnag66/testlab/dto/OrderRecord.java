package com.wnag66.testlab.dto;

import java.time.Instant;

public record OrderRecord(
        String orderId,
        String locationCode,
        String status,
        Instant expiresAt,
        int validatedCount
) {
}

