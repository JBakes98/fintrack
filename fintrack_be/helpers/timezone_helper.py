import datetime
import pytz


def get_timezone(timezone, country_code):
    """
    Method to get the relevant pytz timezone from the country and the timezone such as BST
    :param timezone: The Country timezone
    :param country_code: The Country alpha2 code
    :return: The relevant pytz timezone
    """
    # Check if its a valid timezone already
    if timezone in pytz.all_timezones:
        return timezone

    # If its a number value, use the ETC/GMT code
    try:
        offset = int(timezone)
        # If offset is hours ahead change offset to + not -
        if offset > 0:
            offset = '+' + str(offset)
        else:
            offset = str(offset)
        return 'GMT' + offset

    except ValueError:
        pass

    # Get the abbreviation
    country_tzones = None
    try:
        country_tzones = pytz.country_timezones[country_code] # Gets all timezones for specified country
    except:
        pass

    set_zones = set()
    # Check there are country timezones present
    if country_tzones is not None and len(country_tzones) > 0:
        for name in country_tzones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info',
                                                          [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone.upper():
                    set_zones.add(name)

            if len(set_zones) > 0:
                return min(set_zones, key=len)

                # none matched, at least pick one in the right country
            return min(country_tzones, key=len)

        # invalid country, just try to match the timezone abbreviation to any time zone
        for name in pytz.all_timezones:
            tzone = pytz.timezone(name)
            for utcoffset, dstoffset, tzabbrev in getattr(tzone, '_transition_info',
                                                          [[None, None, datetime.datetime.now(tzone).tzname()]]):
                if tzabbrev.upper() == timezone.upper():
                    set_zones.add(name)

        return min(set_zones, key=len)


def convert_time_to_timezone(dt, tz1, tz2):
    """
    Method that takes a time and converts one timezones time, such as EST and converts it
    to UTC. Method combines time with todays date for conversion to occur.
    :param dt: Time that wants to be converted
    :param tz1: Original timezone of time
    :param tz2: Timezone to translate time to
    :return: Translated datetime object in the second timezone
    """
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.datetime.combine(datetime.date.today(), dt)
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)

    return dt


def convert_datetime_to_timezone(dt, tz1, tz2):
    """
    Method that takes a datetime and converts to one timezones time, such as EST and converts it
    to UTC.
    :param dt: Datetime that wants to be converted
    :param tz1: Original timezone of time
    :param tz2: Timezone to translate time to
    :return: Translated datetime object in the second timezone
    """
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    if dt.tzinfo is None:
        dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)

    return dt
