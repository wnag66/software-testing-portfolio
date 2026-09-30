package com.wnag66.testlab.dto;

import java.time.Instant;

public record ApiError(String code, String message, Instant timestamp) {
}

