def Run( conn, nick, channel, msg ):
	targ = msg.split( " " )[1]
	drink = "a tall, frosty lager."

	if targ.startswith( "JoeDaddy" ):
		drink = "a chilled Twisted Tea."
	elif targ.startswith( "spiffytech" ):
		drink = "an ice-cold diet Coke."
	elif targ.startswith( "Akira" ):
		drink = "two fingers of Glenlivet 18, neat."
	elif targ.startswith( "Sato" ):
		drink = "an iced wine cooler."
	elif targ.startswith( "Rainbarrel" ):
		drink = "a bottle of Crown."
	elif targ.startswith( "zark" ):
		drink = "a cold raspberry lemonade."
	elif targ.startswith( "Hesoj" ):
		drink = "a cool bottle of IBC root beer."

	conn.SendAction( channel, "gets %s %s" % ( targ, drink ) ) 
