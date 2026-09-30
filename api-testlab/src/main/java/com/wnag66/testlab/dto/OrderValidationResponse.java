package com.wnag66.testlab.dto;

import java.time.Instant;

public record OrderValidationResponse(
        String orderId,
        boolean accepted,
        String reason,
        Instant validatedAt
) {
}

