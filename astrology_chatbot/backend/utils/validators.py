def get_zodiac_sign(dob_str: str) -> str:
    month, day = int(dob_str[5:7]), int(dob_str[8:10])
    zodiac_dates = [
        ((1, 20), (2, 18), "aquarius"),
        ((2, 19), (3, 20), "pisces"),
        ((3, 21), (4, 19), "aries"),
        ((4, 20), (5, 20), "taurus"),
        ((5, 21), (6, 20), "gemini"),
        ((6, 21), (7, 22), "cancer"),
        ((7, 23), (8, 22), "leo"),
        ((8, 23), (9, 22), "virgo"),
        ((9, 23), (10, 22), "libra"),
        ((10, 23), (11, 21), "scorpio"),
        ((11, 22), (12, 21), "sagittarius"),
        ((12, 22), (1, 19), "capricorn")
    ]

    for start, end, sign in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "capricorn"
