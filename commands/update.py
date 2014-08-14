import datetime
import os
import math

os.environ['TZ'] = "America/New_York"

def Run( conn, nick, channel, msg ):
	delta = datetime.datetime.combine( datetime.date.today(), datetime.time(17, 30) ) - datetime.datetime.now()

	conn.SendText( channel, "%s: %d minutes, %d seconds until 17:30" % ( nick, math.floor( delta.total_seconds() / 60 ), delta.total_seconds() % 60 ) )


