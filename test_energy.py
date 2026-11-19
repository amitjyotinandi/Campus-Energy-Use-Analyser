import numpy as np
from energy_analyser import is_valid_reading, moving_average, find_spikes, MeterLog, MeterRecord


def test_valid_reading():
    assert is_valid_reading("12.5")
    assert not is_valid_reading("-3")
    assert not is_valid_reading("")
    assert not is_valid_reading("abc")


def test_moving_average():
    out = moving_average([1, 2, 3, 4, 5], window=3)
    assert np.allclose(out, [2.0, 3.0, 4.0])


def test_find_spikes():
    data = [10] * 30 + [500]
    assert list(find_spikes(data)) == [30]


def test_log_len_and_iter():
    log = MeterLog()
    log.add(MeterRecord("2026-01-01", "Library", 100))
    log.add(MeterRecord("2026-01-02", "Library", 110))
    assert len(log) == 2
    assert [r.kwh for r in log] == [100.0, 110.0]


if __name__ == "__main__":
    test_valid_reading(); test_moving_average(); test_find_spikes(); test_log_len_and_iter()
    print("all tests passed")
