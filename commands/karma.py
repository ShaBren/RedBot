def Run( conn, nick, channel, msg ):
	u = conn.r.get_redditor( msg.split( " " )[1] )
	reply = "%s has %d link karma and %d comment karma, for %d total" % ( u.name, u.link_karma, u.comment_karma, u.link_karma + u.comment_karma )

	conn.SendText( channel, "%s: %s" % ( nick, reply ) )
