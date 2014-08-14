def Run( conn, nick, channel, msg ):
	if nick == conn.owner:
		conn.Disconnect() 
	else:
		reply = "Bugger off."

	conn.SendText( channel, "%s: %s" % ( nick, reply ) )
