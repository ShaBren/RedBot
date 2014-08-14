import datetime
import os
import math

os.environ['TZ'] = "America/New_York"

def Run( conn, nick, channel, msg ):
	daily = datetime.datetime.combine( datetime.date.today(), datetime.time(13, 00) ) 

	if daily - datetime.datetime.now() < datetime.timedelta(0):
		daily = datetime.datetime.combine( datetime.date.today() + datetime.timedelta(days=1), datetime.time(13, 00) ) 

	flash = datetime.datetime.combine( datetime.date.today(), datetime.time(5, 00) ) 

	while flash - datetime.datetime.now() < datetime.timedelta(0):
		flash = flash + datetime.timedelta(hours=8)



	dailydelta = daily - datetime.datetime.now()
	flashdelta = flash - datetime.datetime.now()
	conn.SendText( channel, "%s: %d hours, %d minutes, %d seconds until next daily sale. %d hours, %d minutes, %d seconds until next flash sale." % ( 
		nick, 
		math.floor( dailydelta.total_seconds() / 60 / 60 ), math.floor( dailydelta.total_seconds() % 3600 / 60 ), dailydelta.total_seconds() % 60,
		math.floor( flashdelta.total_seconds() / 60 / 60 ), math.floor( flashdelta.total_seconds() % 3600 / 60 ), flashdelta.total_seconds() % 60
	) )
