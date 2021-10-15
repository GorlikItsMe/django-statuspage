import requests
from timeit import default_timer as timer


class CheckReport():
    is_online: bool
    time_ms: int

    def __init__(self, is_online, time_ms):
        self.is_online = is_online
        self.time_ms = int(time_ms)  # round

    def __str__(self) -> str:
        return f"CheckReport(is_online: {self.is_online}, time_ms: {self.time_ms})"


def check_http(url: str, timeout_sek: int) -> CheckReport:
    headers = {
        'User-Agent': 'DjangoStatusPage',
    }
    # start = timer()
    try:
        r = requests.get(url=url, headers=headers, timeout=timeout_sek)
    except Exception:
        return CheckReport(is_online=False, time_ms=0)
    # end = timer()
    # time_ms = (end - start) * 1000
    time_ms = r.elapsed.microseconds * 1000
    if r.status_code == 200:
        return CheckReport(is_online=True, time_ms=time_ms)
    return CheckReport(is_online=False, time_ms=time_ms)  # pragma: no cover <--
