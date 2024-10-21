from random import randint

def generate_date(start_year, end_year) -> str:
    year = str(randint(start_year, end_year))
    month = randint(1, 12)

    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    day = randint(1, 28)

    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    return day + '.' + month + '.' + year

def generate_username(custom_url: str) -> str:
    return custom_url.split('@')[1]

def generate_email(username: str) -> str:
    return username + '@gmail.com'
