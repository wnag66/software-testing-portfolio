package com.wnag66.testlab.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;

public record HeartbeatRequest(
        @NotBlank String status,
        @NotNull Instant timestamp,
        @NotNull Integer latencyMs
) {
}

