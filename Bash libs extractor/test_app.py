 
import subprocess
import pytest
from app import error_window


def test_ldd_available():
    result = subprocess.run(["which", "ldd"], capture_output=True, text=True)
    assert result.returncode == 0, "ldd не найден в системе"


def test_error_window_creates():
    try:
        error_window("1")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове окна: {e}")
