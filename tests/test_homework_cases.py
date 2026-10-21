"""Additional cases derived from requirements 5, 6, 7 and 8."""
import pytest

@pytest.mark.parametrize("value", [2, 49, 98])
def test_additional_valid_pwm(device, value):
    reply = device.command(f"SET PWM {value}")
    assert reply["status"] == "OK", reply
    assert reply["pwm"] == value, reply

@pytest.mark.parametrize("value", [-100, -2, 102, 1000])
def test_invalid_pwm_preserves_safe_state(device, value):
    reply = device.command(f"SET PWM {value}")
    assert reply["status"] == "ERROR", reply
    assert reply["code"] == "INVALID_VALUE", reply
    state = device.command("STATUS")
    assert state["led"] is False and state["pwm"] == 0, state

@pytest.mark.parametrize("command", ["FOO", "GET UNKNOWN", "SET UNKNOWN 1"])
def test_unknown_command_is_structured_error(device, command):
    reply = device.command(command)
    assert reply["status"] == "ERROR", reply
    assert reply["code"] == "UNKNOWN_COMMAND", reply

@pytest.mark.parametrize("prepare", ["SET LED ON", "SET PWM 50", "SET PWM 99"])
def test_reset_after_active_output(device, prepare):
    assert device.command(prepare)["status"] == "OK"
    before = device.command("STATUS")
    assert before["led"] is True and before["pwm"] > 0, before
    assert device.command("RESET")["status"] == "OK"
    after = device.command("STATUS")
    assert after["led"] is False and after["pwm"] == 0, after
