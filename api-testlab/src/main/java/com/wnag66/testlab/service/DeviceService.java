package com.wnag66.testlab.service;

import com.wnag66.testlab.dto.DeviceStatusResponse;
import com.wnag66.testlab.dto.HeartbeatRequest;
import com.wnag66.testlab.exception.InvalidRequestException;
import com.wnag66.testlab.exception.ResourceNotFoundException;
import com.wnag66.testlab.repository.DeviceRepository;
import org.springframework.stereotype.Service;

import java.util.Locale;
import java.util.Set;
import java.util.regex.Pattern;

@Service
public class DeviceService {

    private static final Pattern DEVICE_ID = Pattern.compile("^D\\d{3}$");
    private static final Set<String> VALID_STATUSES = Set.of("ONLINE", "OFFLINE", "DEGRADED");

    private final DeviceRepository deviceRepository;

    public DeviceService(DeviceRepository deviceRepository) {
        this.deviceRepository = deviceRepository;
    }

    public DeviceStatusResponse getStatus(String deviceId) {
        validateDeviceId(deviceId);
        return deviceRepository.findById(deviceId)
                .orElseThrow(() -> new ResourceNotFoundException("Device " + deviceId + " was not found"));
    }

    public DeviceStatusResponse heartbeat(String deviceId, HeartbeatRequest request) {
        validateDeviceId(deviceId);
        String status = request.status().toUpperCase(Locale.ROOT);
        if (!VALID_STATUSES.contains(status)) {
            throw new InvalidRequestException("status is not supported");
        }
        if (!deviceRepository.findById(deviceId).isPresent()) {
            throw new ResourceNotFoundException("Device " + deviceId + " was not found");
        }
        deviceRepository.updateHeartbeat(deviceId, status, request.timestamp(), request.latencyMs());
        return getStatus(deviceId);
    }

    private void validateDeviceId(String deviceId) {
        if (deviceId == null || !DEVICE_ID.matcher(deviceId).matches()) {
            throw new InvalidRequestException("deviceId must match D followed by three digits");
        }
    }
}

