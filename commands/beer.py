def Run( conn, nick, channel, msg ):
	targ = msg.split( " " )[1]
	conn.SendAction( channel, "gets %s a tall, frosty lager." % ( targ, ) ) 
