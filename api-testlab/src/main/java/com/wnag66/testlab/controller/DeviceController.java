package com.wnag66.testlab.controller;

import com.wnag66.testlab.dto.DeviceStatusResponse;
import com.wnag66.testlab.dto.HeartbeatRequest;
import com.wnag66.testlab.service.DeviceService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/devices")
public class DeviceController {

    private final DeviceService deviceService;

    public DeviceController(DeviceService deviceService) {
        this.deviceService = deviceService;
    }

    @GetMapping("/{deviceId}/status")
    public DeviceStatusResponse getStatus(@PathVariable String deviceId) {
        return deviceService.getStatus(deviceId);
    }

    @PostMapping("/{deviceId}/heartbeat")
    public DeviceStatusResponse heartbeat(
            @PathVariable String deviceId,
            @Valid @RequestBody HeartbeatRequest request
    ) {
        return deviceService.heartbeat(deviceId, request);
    }
}

