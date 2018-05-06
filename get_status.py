#!/usr/bin/python3

from pushbullet import Pushbullet
from bs4 import BeautifulSoup
import requests

status = {}

r = BeautifulSoup(requests.get("https://status.digitalocean.com/").text, "html.parser")

for n in r.find_all("span", attrs={"class":"name"}):
	try:
		print(n.string.strip())
		if n.string.strip() == "SFO2" or n.string.strip() == "Droplets":
			print(n.parent.find("span", attrs={"class":"component-status"}).string.strip())

			status[n.string.strip()] = n.parent.find("span", attrs={"class":"component-status"}).string.strip()

		print("")
	except AttributeError:
		continue

print(status)
for x in status:
	if status[x] != "Operational":
		push = Pushbullet(os.environ.get('pushbullet_apikey')).push_note("DigitalOcean Status", x + " is NOT operational at the current moment. Checking again in FIVE minutes...")
