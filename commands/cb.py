import xmlrpc.client

proxy = xmlrpc.client.ServerProxy( "http://localhost:12929/" )

def Run( conn, nick, channel, msg ):
	print( msg )
	resp = proxy.respond( msg, nick )
	conn.SendText( channel, "%s: %s" % ( nick, resp ) )
