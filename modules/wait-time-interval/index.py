import time

def wait_time_interval(seconds: float) -> dict:
    if seconds < 0:
        raise ValueError("Khoảng thời gian không thể nhỏ hơn 0")

    start = time.time()
    time.sleep(seconds)
    elapsed = time.time() - start

    return {
        "elapsed": round(elapsed, 4),
        "completed": True
    }
