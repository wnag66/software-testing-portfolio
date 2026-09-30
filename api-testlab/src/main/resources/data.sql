INSERT INTO devices (device_id, device_name, location_code, status, last_heartbeat, latency_ms)
VALUES
    ('D001', 'East Gate Reader', 'L001', 'ONLINE', CURRENT_TIMESTAMP, 85),
    ('D002', 'West Gate Reader', 'L001', 'OFFLINE', CURRENT_TIMESTAMP, 0),
    ('D003', 'Service Kiosk', 'L002', 'DEGRADED', CURRENT_TIMESTAMP, 430);

INSERT INTO orders (order_id, location_code, status, expires_at, validated_count)
VALUES
    ('O1001', 'L001', 'CREATED', TIMESTAMP WITH TIME ZONE '2099-12-31 23:59:59+08:00', 0),
    ('O1002', 'L001', 'CREATED', TIMESTAMP WITH TIME ZONE '2020-01-01 00:00:00+08:00', 0);

INSERT INTO events (event_type, severity, location_code, occurred_at, message)
SELECT
    CASE WHEN X % 3 = 0 THEN 'ALERT' WHEN X % 3 = 1 THEN 'HEARTBEAT' ELSE 'ORDER' END,
    CASE WHEN X % 4 = 0 THEN 'HIGH' WHEN X % 4 = 1 THEN 'MEDIUM' ELSE 'LOW' END,
    CASE WHEN X % 2 = 0 THEN 'L001' ELSE 'L002' END,
    DATEADD('MINUTE', -X, CURRENT_TIMESTAMP),
    CONCAT('Seed event ', X)
FROM SYSTEM_RANGE(1, 64) AS r(x);
