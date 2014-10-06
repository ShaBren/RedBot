def Run( conn, nick, channel, msg ):
	parts = msg.split( " " )

	if len( parts ) < 2:
		conn.SendText( channel, "%s: Usage: `karma <username>" % ( nick, ) )
		return

	try:
		u = conn.r.get_redditor( parts[1] )
	except:
		u = None

	if not u:
		conn.SendText( channel, "%s: User not found" % ( nick, ) )
		return

	reply = "%s has %d link karma and %d comment karma, for %d total" % ( u.name, u.link_karma, u.comment_karma, u.link_karma + u.comment_karma )

	conn.SendText( channel, "%s: %s" % ( nick, reply ) )
