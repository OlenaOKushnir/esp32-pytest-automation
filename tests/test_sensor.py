import math
import os
import time

import pytest

def test_temperature_is_valid_json(device):
    r = device.command("GET TEMP")
    assert r["status"] in {"OK", "ERROR"}
    if r["status"] == "OK":
        assert -40 <= r["temperature"] <= 80

@pytest.fixture
def expected_temperature():
    raw = os.getenv("EXPECTED_TEMP_C")
    if raw is None:
        pytest.skip("Set EXPECTED_TEMP_C to the controlled sensor temperature")
    try:
        expected = float(raw)
    except ValueError:
        pytest.fail("EXPECTED_TEMP_C must be a finite number")
    assert math.isfinite(expected), "EXPECTED_TEMP_C must be finite"
    return expected


@pytest.mark.parametrize("sample", [1, 2, 3], ids=["sample-1", "sample-2", "sample-3"])
def test_sensor_matches_controlled_temperature(expected_temperature, device, sample):
    # Use a controlled stimulus, not a blanket prohibition of valid 0 C readings.
    # Each case has its own safe-state fixture and waits before acquiring a sample.
    time.sleep(2.1)
    reply = device.command("GET TEMP")
    assert reply["status"] == "OK", f"Sensor must be available: {reply!r}"
    value = reply.get("temperature")
    assert type(value) in (int, float), f"Non-numeric temperature: {reply!r}"
    assert math.isfinite(value), f"Non-finite temperature: {reply!r}"
    assert value == pytest.approx(expected_temperature, abs=0.5), (
        f"Sample {sample}: expected {expected_temperature} +/- 0.5 C; got {value}. "
        "Check sensor stimulus, connection, and firmware."
    )