import random, datetime as dt
def dias(y, m, n):
    ult = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    tope = 9 if (y, m) == (2026, 10) else ult
    hab = [dt.date(y, m, d) for d in range(1, tope + 1) if dt.date(y, m, d).weekday() != 6]
    return sorted(random.choice(hab) for _ in range(n))
