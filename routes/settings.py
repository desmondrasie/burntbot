import flask

import globals

from utilities.persistence import upsert_persistence

def settings_page():
	data = {
		'version': globals.version,
		'poll_rate': globals.bot_poll_rate,
		'note': globals.bot_note,
		'return_check': globals.bot_return_check,
		'shaking_sats_enabled': globals.shaking_sats_enabled
	}

	return flask.render_template('settings.html', data = data)

def settings_save():
	save_data = {}
	data = flask.request.get_json()

	# dont know if this is the right choice for validation:
	# i am only checking for certain keys and saving those while ignoring the rest

	if ('note' in data):
		save_data['note'] = data['note']
		globals.bot_note = data['note']

	# also make sure poll rate doesnt break API rate limit
	if ('poll_rate' in data):
		cast_poll_rate = float(data['poll_rate'])

		if (cast_poll_rate < 4):
			flask.Response(status = 400)
		else:
			save_data['poll_rate'] = cast_poll_rate
			globals.bot_poll_rate = cast_poll_rate

	if ('return_check' in data):
		save_data['bot_return_check'] = data['return_check']
		globals.bot_return_check = data['return_check']

	if ('shaking_sats_enabled' in data):
		save_data['shaking_sats_enabled'] = data['shaking_sats_enabled']
		globals.shaking_sats_enabled = data['shaking_sats_enabled']

	upsert_persistence(save_data)
	
	return flask.Response(status = 201)