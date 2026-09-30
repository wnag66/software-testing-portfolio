package com.wnag66.testlab.repository;

import com.wnag66.testlab.dto.OrderRecord;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public class OrderRepository {

    private final JdbcTemplate jdbcTemplate;

    public OrderRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Optional<OrderRecord> findById(String orderId) {
        List<OrderRecord> results = jdbcTemplate.query("""
                SELECT order_id, location_code, status, expires_at, validated_count
                FROM orders
                WHERE order_id = ?
                """, (resultSet, rowNum) -> new OrderRecord(
                resultSet.getString("order_id"),
                resultSet.getString("location_code"),
                resultSet.getString("status"),
                resultSet.getTimestamp("expires_at").toInstant(),
                resultSet.getInt("validated_count")
        ), orderId);
        return results.stream().findFirst();
    }

    public void incrementValidatedCount(String orderId) {
        jdbcTemplate.update("UPDATE orders SET validated_count = validated_count + 1 WHERE order_id = ?", orderId);
    }
}

