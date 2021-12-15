from time_diffrence import minutes_to_seconds, hours_to_minutes, hhmm_to_seconds, time_difference_in_seconds

def test_minutes_to_seconds():
    data = minutes_to_seconds(1)
    assert data == 60
def test_hours_to_minutes():
    data = hours_to_minutes(1)
    assert data == 60
def test_hhmm_to_seconds():
    data = hhmm_to_seconds("01:01")
    assert data == 3660

def test_time_difference_in_seconds():
    data = time_difference_in_seconds("00:00")
    assert isinstance(data, int)
    
if __name__ == "__main__":
    test1 = test_minutes_to_seconds()
    test2 = test_hours_to_minutes()
    test3 = test_hhmm_to_seconds()
    test4 = test_time_difference_in_seconds()