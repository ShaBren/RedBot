def Run( conn, nick, channel, msg ):
	conn.SendText( channel, "%s: Commands: %s" % ( nick, ", ".join( conn.commands.keys() ) ) )
