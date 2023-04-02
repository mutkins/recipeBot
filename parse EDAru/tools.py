import re


def get_minutes_from_mixed_string(mixed_string):
    minutes = 0

    for item in re.findall('\d+\s\S+', mixed_string):
        if re.search('\d+\sчас', item):
            res = re.search('\d+', item).group(0)
            minutes += int(res)*60

        if re.search('\d+\sмину', item):
            res = re.search('\d+', item).group(0)
            minutes += int(res)

        if re.search('\d+\sсут', item):
            res = re.search('\d+', item).group(0)
            minutes += int(res)*1440
    return minutes