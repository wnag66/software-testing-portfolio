package com.wnag66.testlab.repository;

import com.wnag66.testlab.dto.EventResponse;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public class EventRepository {

    private final JdbcTemplate jdbcTemplate;

    public EventRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<EventResponse> search(String type, String severity, String locationCode, int size, int offset) {
        StringBuilder sql = new StringBuilder("""
                SELECT event_id, event_type, severity, location_code, occurred_at, message
                FROM events
                WHERE 1 = 1
                """);
        List<Object> parameters = new ArrayList<>();
        appendFilter(sql, parameters, "event_type", type);
        appendFilter(sql, parameters, "severity", severity);
        appendFilter(sql, parameters, "location_code", locationCode);
        sql.append(" ORDER BY occurred_at DESC, event_id DESC LIMIT ? OFFSET ?");
        parameters.add(size);
        parameters.add(offset);
        return jdbcTemplate.query(sql.toString(), (resultSet, rowNum) -> new EventResponse(
                resultSet.getLong("event_id"),
                resultSet.getString("event_type"),
                resultSet.getString("severity"),
                resultSet.getString("location_code"),
                resultSet.getTimestamp("occurred_at").toInstant(),
                resultSet.getString("message")
        ), parameters.toArray());
    }

    public long count(String type, String severity, String locationCode) {
        StringBuilder sql = new StringBuilder("SELECT COUNT(*) FROM events WHERE 1 = 1");
        List<Object> parameters = new ArrayList<>();
        appendFilter(sql, parameters, "event_type", type);
        appendFilter(sql, parameters, "severity", severity);
        appendFilter(sql, parameters, "location_code", locationCode);
        Long count = jdbcTemplate.queryForObject(sql.toString(), Long.class, parameters.toArray());
        return count == null ? 0 : count;
    }

    private void appendFilter(StringBuilder sql, List<Object> parameters, String column, String value) {
        if (value != null && !value.isBlank()) {
            sql.append(" AND ").append(column).append(" = ?");
            parameters.add(value);
        }
    }
}

