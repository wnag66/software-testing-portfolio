package com.wnag66.testlab.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;

public record OrderValidationRequest(
        @NotBlank String locationCode,
        @NotBlank String gateId,
        @NotNull Instant validatedAt
) {
}

