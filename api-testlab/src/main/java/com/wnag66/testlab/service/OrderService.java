package com.wnag66.testlab.service;

import com.wnag66.testlab.dto.OrderRecord;
import com.wnag66.testlab.dto.OrderValidationRequest;
import com.wnag66.testlab.dto.OrderValidationResponse;
import com.wnag66.testlab.exception.InvalidRequestException;
import com.wnag66.testlab.exception.ResourceNotFoundException;
import com.wnag66.testlab.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.regex.Pattern;

@Service
public class OrderService {

    private static final Pattern ORDER_ID = Pattern.compile("^O\\d{4}$");

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public OrderValidationResponse validate(String orderId, OrderValidationRequest request) {
        if (orderId == null || !ORDER_ID.matcher(orderId).matches()) {
            throw new InvalidRequestException("orderId must match O followed by four digits");
        }
        if (!"L001".equals(request.locationCode())) {
            throw new InvalidRequestException("locationCode is not available in this test lab");
        }
        OrderRecord order = orderRepository.findById(orderId)
                .orElseThrow(() -> new ResourceNotFoundException("Order " + orderId + " was not found"));
        if (!"CREATED".equals(order.status()) || order.expiresAt().isBefore(request.validatedAt())) {
            return new OrderValidationResponse(orderId, false, "EXPIRED", request.validatedAt());
        }
        orderRepository.incrementValidatedCount(orderId);
        return new OrderValidationResponse(orderId, true, "VALID", request.validatedAt());
    }
}

