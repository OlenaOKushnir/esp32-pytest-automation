import logging
import os

import pytest
from device import Device

log = logging.getLogger(__name__)


def refresh_initial_state(dev):
    """Restore and verify a known output state independently of RESET behavior."""
    log.info("Restoring initial state: LED OFF, PWM 0")
    for command in ("RESET", "SET LED OFF", "SET PWM 0"):
        reply = dev.command(command)
        assert reply.get("status") == "OK", f"{command} failed: {reply!r}"
    state = dev.command("STATUS")
    assert state.get("status") == "OK", state
    assert state.get("led") is False, f"LED is not OFF: {state!r}"
    assert type(state.get("pwm")) is int and state["pwm"] == 0, (
        f"PWM is not zero: {state!r}"
    )
    log.info("Initial state verified: %r", state)
    return state


@pytest.fixture
def device():
    port = os.getenv("DEVICE_PORT")
    if not port:
        pytest.skip("Set DEVICE_PORT to a COM port or Wokwi RFC2217 URL")
    dev = Device(port, timeout=1.0)
    try:
        refresh_initial_state(dev)
        yield dev
    finally:
        try:
            refresh_initial_state(dev)
        finally:
            dev.close()
