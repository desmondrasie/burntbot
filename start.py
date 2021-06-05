#!/usr/bin/python3

import time
import sys

import globals
import bot

from service.requests.wallet import get_wallet
from service.persistence import read_persistence, upsert_persistence
from service.log import log

if (__name__ == '__main__'):
	for arg in sys.argv:
		if (arg == '-v'):
			globals.flags['verbose'] = True
		elif (arg == '-l'):
			globals.flags['listen'] = True
		else:
			log(f'Unknown argument: {arg}')
			raise SystemExit(0)

	persistence = {}

	# read or create persistence file
	try:
		log('Reading persistence file')
		persistence = read_persistence()
	except:
		log('Creating new persistence file')

		# save defaults
		persistence = {
			'token': '',
			'poll_rate': globals.poll_rate,
			'note': globals.note
		}

		upsert_persistence(persistence)

	# check if the file is valid (we have token key)
	if (not 'token' in persistence) or (persistence['token'] == ''):
		log('No token found, stopping')
		raise SystemExit(0)
	
	# set global variables
	globals.note = persistence['note'] or globals.note
	globals.poll_rate = persistence['poll_rate'] or globals.poll_rate

	# set the authorization header
	globals.headers['Authorization'] = persistence['token']

	# validate valid token by getting wallet ID
	log('Getting CAD wallet ID')
	globals.wallet_id = get_wallet()['id']

	# start bot thread
	log('Starting bot')

	bot = bot.SwapBot()
	bot.start()

	# main thread busy
	while (1):
		if (not bot.is_alive()):
			log('Bot died, stopping')
			break

		time.sleep(10)