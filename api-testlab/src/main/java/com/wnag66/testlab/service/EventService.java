package com.wnag66.testlab.service;

import com.wnag66.testlab.dto.EventResponse;
import com.wnag66.testlab.dto.PageResponse;
import com.wnag66.testlab.exception.InvalidRequestException;
import com.wnag66.testlab.repository.EventRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Locale;
import java.util.Set;

@Service
public class EventService {

    private static final Set<String> TYPES = Set.of("ALERT", "HEARTBEAT", "ORDER");
    private static final Set<String> SEVERITIES = Set.of("LOW", "MEDIUM", "HIGH");

    private final EventRepository eventRepository;

    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    public PageResponse<EventResponse> search(
            String type,
            String severity,
            String locationCode,
            int page,
            int size
    ) {
        if (page < 1) {
            throw new InvalidRequestException("page must be greater than or equal to 1");
        }
        String normalizedType = normalize(type);
        String normalizedSeverity = normalize(severity);
        validateAllowed("type", normalizedType, TYPES);
        validateAllowed("severity", normalizedSeverity, SEVERITIES);
        int offset = (page - 1) * size;
        List<EventResponse> items = eventRepository.search(
                normalizedType,
                normalizedSeverity,
                locationCode,
                size,
                offset
        );
        long total = eventRepository.count(normalizedType, normalizedSeverity, locationCode);
        long pageCount = total / size;
        return new PageResponse<>(items, page, size, total, pageCount);
    }

    private String normalize(String value) {
        return value == null || value.isBlank() ? null : value.toUpperCase(Locale.ROOT);
    }

    private void validateAllowed(String field, String value, Set<String> allowed) {
        if (value != null && !allowed.contains(value)) {
            throw new InvalidRequestException(field + " is not supported");
        }
    }
}

