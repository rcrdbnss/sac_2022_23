import re
from datetime import datetime
import random
from uuid import UUID

PRJ_DATE_FMT = '%Y-%m-%dT%H:%M:%SZ'


def date_from_str(date_string: str, format=PRJ_DATE_FMT):
	try:
		return datetime.strptime(date_string, format)
	except ValueError:
		return None


def str_from_date(date: datetime, format=PRJ_DATE_FMT):
	return date.strftime(format)


def uuid_from_str(uuid_str: str, version=4):
	try:
		return UUID(uuid_str, version=version)
	except ValueError:
		return None


def is_email(email: str):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	return re.fullmatch(regex, email)


def secret_santa_pairs(names: list):
	while True:
		targets = random.sample(names, len(names))
		if not any(a == b for a, b in zip(targets, names)):
			return zip(targets, names)
