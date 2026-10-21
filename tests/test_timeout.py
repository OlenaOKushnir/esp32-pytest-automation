import time
import pytest

def test_no_response_becomes_timeout(device):
    assert device.ser.timeout is not None and 0 < device.ser.timeout <= 1.0
    started = time.monotonic()
    with pytest.raises(TimeoutError):
        device.command("NO_RESPONSE")
    elapsed = time.monotonic() - started
    assert elapsed >= device.ser.timeout * 0.8, elapsed
    assert elapsed < device.ser.timeout + 2.0, elapsed
