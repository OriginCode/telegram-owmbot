__all__ = []


def __deghandler__(deg):
    if 330 <= deg <= 360 or 0 <= deg < 30:
        return "N"

    elif 30 <= deg < 60:
        return "NE"

    elif 60 <= deg < 120:
        return "E"

    elif 120 <= deg < 150:
        return "SE"

    elif 150 <= deg < 210:
        return "S"

    elif 210 <= deg < 240:
        return "SW"

    elif 240 <= deg < 300:
        return "W"

    elif 300 <= deg < 330:
        return "NW"
