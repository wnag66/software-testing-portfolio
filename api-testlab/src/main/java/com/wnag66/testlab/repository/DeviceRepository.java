package com.wnag66.testlab.repository;

import com.wnag66.testlab.dto.DeviceStatusResponse;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.sql.Timestamp;
import java.util.List;
import java.util.Optional;

@Repository
public class DeviceRepository {

    private final JdbcTemplate jdbcTemplate;

    public DeviceRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Optional<DeviceStatusResponse> findById(String deviceId) {
        List<DeviceStatusResponse> results = jdbcTemplate.query("""
                SELECT device_id, device_name, location_code, status, last_heartbeat, latency_ms
                FROM devices
                WHERE device_id = ?
                """, (resultSet, rowNum) -> new DeviceStatusResponse(
                resultSet.getString("device_id"),
                resultSet.getString("device_name"),
                resultSet.getString("location_code"),
                resultSet.getString("status"),
                resultSet.getTimestamp("last_heartbeat").toInstant(),
                resultSet.getInt("latency_ms")
        ), deviceId);
        return results.stream().findFirst();
    }

    public void updateHeartbeat(String deviceId, String status, java.time.Instant timestamp, int latencyMs) {
        jdbcTemplate.update("""
                UPDATE devices
                SET status = ?, last_heartbeat = ?, latency_ms = ?
                WHERE device_id = ?
                """, status, Timestamp.from(timestamp), latencyMs, deviceId);
    }
}

