def Run( conn, nick, channel, msg ):
	conn.SendText( channel, "%s: pong" % ( nick, ) )
