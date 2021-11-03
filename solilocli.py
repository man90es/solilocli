#!/usr/bin/python

import argparse
import csv
import requests
from datetime import date, datetime
from pathlib import Path


class cmdTags:
	BLUE = "\033[94m"
	BOLD = "\033[1m"
	END =  "\033[0m"


def print_row(row, dateFmt):
	if len(dateFmt) > 0:
		date_str = cmdTags.BLUE + date.today().strftime(dateFmt) + cmdTags.END
		print("\r" + "Today is", date_str)
	pass

	word = cmdTags.BOLD + row[0] + cmdTags.END
	pos = "(" + row[1] + ")"
	definition = row[2]
	print("Word of the day:", word, pos, "—", definition, "\n")


def get_timestamp():
	dt = datetime.combine(date.today(), datetime.min.time())
	return round(datetime.timestamp(dt))


def parse_args():
	parser = argparse.ArgumentParser(description="Print a word of the day")

	parser.add_argument(
		"-n", dest="n", action="store_const",
		const=True, default=False, help="Dont' use cache"
	)
	parser.add_argument(
		"-d", dest="d",
		default="%A, %B %-d", help="Specify date format"
	)
	parser.add_argument(
		"-e", dest="e",
		default="https://soliloquy.hemlo.cc", help="Specify the API endpoint"
	)

	return parser.parse_args()


if __name__ == "__main__":
	timestamp = get_timestamp()
	args = parse_args()
	cache = Path("/tmp/wod-cache-" + str(timestamp))
	use_cache = not args.n and cache.is_file()

	# Print string from cache if it's allowed and exists
	if (use_cache):
		with open(cache, "r") as csvfile:
			print_row(list(csv.reader(csvfile, delimiter="|"))[0], args.d)

	# Request a string from the server
	else:
		p = {"ts": timestamp}
		h = {"Accept": "text/plain"}
		r = requests.get(url=args.e, params=p, headers=h, timeout=3)

		print_row(list(csv.reader([r.text], delimiter="|"))[0], args.d)

		# Write cache
		if (not args.n):
			with open(cache, "w") as csvfile:
				csvfile.write(r.text)
