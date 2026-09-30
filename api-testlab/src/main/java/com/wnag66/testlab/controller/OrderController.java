package com.wnag66.testlab.controller;

import com.wnag66.testlab.dto.OrderValidationRequest;
import com.wnag66.testlab.dto.OrderValidationResponse;
import com.wnag66.testlab.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping("/{orderId}/validate")
    public OrderValidationResponse validate(
            @PathVariable String orderId,
            @Valid @RequestBody OrderValidationRequest request
    ) {
        return orderService.validate(orderId, request);
    }
}

