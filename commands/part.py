def Run( conn, nick, channel, msg ):
	if nick == conn.owner:
		conn.Part( msg.split( " " )[1] ) 
	else:
		reply = "Bugger off."
		conn.SendText( channel, "%s: %s" % ( nick, reply ) )
	

