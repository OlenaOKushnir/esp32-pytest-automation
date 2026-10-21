"""Transport checks only; these do not establish firmware behavior."""
import pytest
from device import Device

class SilentSerial:
    def reset_input_buffer(self):
        pass
    def write(self, data):
        self.written = data
    def flush(self):
        pass
    def readline(self):
        return b""

@pytest.mark.parametrize("command", ["PING", "STATUS", "NO_RESPONSE"])
def test_empty_serial_response_raises_timeout(command):
    dev = Device.__new__(Device)
    dev.ser = SilentSerial()
    with pytest.raises(TimeoutError, match="No response for command"):
        dev.command(command)
    assert dev.ser.written == (command + "\n").encode()
