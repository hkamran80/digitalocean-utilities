# DigitalOcean Status (v2)

from pushbullet import Pushbullet
from bs4 import BeautifulSoup
import requests

status = {}
checkup = [] # Names of stuff to checkup on here (see status.digitalocean.com for a list)
pb_apikey = "" # Pushbullet API key goes here, optional

r = BeautifulSoup(requests.get("https://status.digitalocean.com/").text, "html.parser")

for n in r.find_all("span", attrs={"class":"name"}):
	try:
		if n.string.strip() in checkup:
			status[n.string.strip()] = n.parent.find("span", attrs={"class":"component-status"}).string.strip()

			if n.parent.find("span", attrs={"class":"component-status"}).string.strip() == "Operational":
				print("\033[1m" + n.string.strip() + "\x1B[0m: \033[92mOperational\x1B[0m")
			else:
				print("\033[1m" + n.string.strip() + "\x1B[0m: \033[91mNot Operational\x1B[0m")
		else:
			if n.parent.find("span", attrs={"class":"component-status"}).string.strip() == "Operational":
				print(n.string.strip() + ": \033[92mOperational\x1B[0m")
			else:
				print(n.string.strip() + ": \033[91mNot Operational\x1B[0m")

		#print("")
	except AttributeError:
		continue

print("")

print(status)

if pb_apikey != "":
	for c in status:
		if status[c] != "Operational":
			push = Pushbullet(pb_apikey).push_note("DigitalOcean Status", "'" + c + "' is NOT operational at the current moment.")
