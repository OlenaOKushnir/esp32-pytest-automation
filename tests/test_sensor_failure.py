import os
import time

import pytest


@pytest.mark.skipif(
    os.getenv("SENSOR_FAILURE_TEST") != "1",
    reason="Requires disconnected DHT22 data line",
)
def test_disconnected_sensor_returns_explicit_error(device):
    # Allow the sensor read interval to elapse.
    time.sleep(2.1)

    response = device.command("GET TEMP")

    assert response["status"] == "ERROR", response
    assert response["code"] == "SENSOR_UNAVAILABLE", response
    assert "temperature" not in response, response