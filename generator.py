from random import randint


def generate_date(start_year: int, end_year: int) -> str:
    year = str(randint(start_year, end_year))
    month = transform_view(randint(1, 12))
    day = transform_view(randint(1, 28))
    return day + "." + month + "." + year


def transform_view(num: int) -> str:
    return str(num) if num >= 10 else "0" + str(num)


def generate_username(custom_url: str) -> str:
    return custom_url.split("@")[1]


def generate_email(username: str) -> str:
    return username + "@gmail.com"
