from datetime import datetime
from uuid import UUID

HR_DATE_FMT = '%d-%m-%Y'


def date_from_str(date_string: str, format=HR_DATE_FMT):
	try:
		return datetime.strptime(date_string, format)
	except ValueError:
		return None


def str_from_date(date: datetime, format=HR_DATE_FMT):
	return date.strftime(format)


def uuid_from_str(uuid_str: str, version=4):
	try:
		return UUID(uuid_str, version=version)
	except ValueError:
		return None