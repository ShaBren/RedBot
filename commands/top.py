def Run( conn, nick, channel, msg ):
	parts = msg.split( " " )
	subreddit = "all"

	if len( parts ) > 1:
		subreddit = parts[1]

	if "/" in subreddit:
		subreddit = subreddit.rpartition( "/" )[2]

	post = next( conn.r.get_subreddit( subreddit ).get_top( limit=1 ), None )

	if post:
		reply = "[/r/%s] \"%s\" with %d comments - %s" % ( post.subreddit.display_name, post.title, post.num_comments, post.short_link )
	else:
		reply = "Unable to find post"

	conn.SendText( channel, "%s: %s" % ( nick, reply ) )
