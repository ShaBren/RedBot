def Run( conn, nick, channel, msg ):
	args = msg.split( " " )

	if len( args ) < 3:
		conn.SendText( channel, "%s: Usage: tip <user> <amount>" % ( nick, ) )
		return

	dest = args[1]
	amount = int( args[2] )

	if amount <= 0:
		conn.SendText( "%s: %d is an invalid amount" % ( nick, amount ) )
		return

	c = conn.db.cursor()
	c.execute( "SELECT * FROM tip_user WHERE name=?", dest )

	destacct = c.fetchone()

	if not destacct:
		conn.SendText( channel, "%s: User %s does not exist" % ( nick, dest ) )
		return

	c.execute( "SELECT * FROM tip_user WHERE name=?", nick )

	srcacct = c.fetchone()

	if not srcacct:
		conn.SendText( channel, "%s: User %s does not exist" % ( nick, nick ) )
		return

	if srcacct['balance'] < amount:
		conn.SendText( channel, "%s: Insufficient funds. You've been charged a 5 internets NSF fee." % ( nick, ) )
		conn.execute( "UPDATE tip_user SET balance=? WHERE name=?", ( srcacct['balance'] - 5, nick ) )
		return

	conn.execute( "UPDATE tip_user SET balance=? WHERE name=?", ( srcacct['balance'] - amount, nick ) )
	conn.execute( "UPDATE tip_user SET balance=? WHERE name=?", ( destacct['balance'] + amount, dest ) )

	conn.SendText( channel, "%s -> %s %d internets VERIFIED" % ( nick, dest, amount ) ) 
