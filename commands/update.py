import datetime
import os
import math

os.environ['TZ'] = "America/New_York"

def GetDeltaTime( hour, minute ):
	delta = datetime.datetime.combine( datetime.date.today(), datetime.time( hour, minute ) ) - datetime.datetime.now()
	return ( math.floor( delta.total_seconds() / 60 ), delta.total_seconds() % 60 )

def Run( conn, nick, channel, msg ):
	hour = 17
	minute = 30

	day = datetime.datetime.today().weekday()

	if nick.startswith( "zark" ):
		hour = 17
		minute = 30
	elif nick.startswith( "Sato" ):
		if day == 0 or day == 1:
			hour = 20
			minute = 0
		elif day == 3 or day == 4:
			hour = 17
			minute = 30
		elif day == 5:
			hour = 16
			minute = 30
	elif nick.startswith( "Sha`Bren" ):
		hour = 18
		minute = 30

	delta = GetDeltaTime( hour, minute )

	conn.SendText( channel, "%s: %d minutes, %d seconds until %02d:%02d" % ( nick, delta[0], delta[1], hour, minute ) )


