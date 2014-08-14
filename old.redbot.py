from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor

import ConfigParser

class redbot( irc.IRCClient ):

	def __init__( self ):
		self.channels = []
		self.config = self.factory.config

		channels = self.config.get( "IRC", "channels" )
		self.commandPrefix = self.config.get( "IRC", "command_prefix" )

		for channel in channels.split( ',' ):
			self.channels.append( channel.strip() )

	def _get_nickname( self ):
		return self.factory.nickname

	nickname = property( _get_nickname )

	def signedOn( self ):
		print( "Signed on as " + self.nickname )

		for channel in self.channels:
			self.join( channel )

	def joined( self, channel ):
		print( "Joined " + channel )

	def action( self, user, channel, msg ):
		if not user:
			return

		#msgFrom = user.split( '!', 1 )[0]

	def privmsg( self, user, channel, msg ):
		if not user:
			return

		reply = ""

		msgFrom = user.split( '!', 1 )[0]

		if msg.startswith( self.commandPrefix ):
			reply = self.parseMsg( msg[1:], channel, msgFrom )
		elif msg.startswith( self.nickname ):
			reply = self.parseMsg( " ".join( msg.split( " " )[1:] ), channel, msgFrom )

		if reply != None and len( reply ) > 0:
			replyMsg = "%s: %s" % ( msgFrom, reply )
			self.msg( channel, replyMsg )

	def parseMsg( self, msg, channel, user ): 

		if msg.startswith( "source" ):
			return self.config.get( "General", "source_url" )

		if msg.startswith( "yo" ):
			return msg

		elif msg.startswith( "help" ):
			return "I'm a Reddit bot type thing."

		elif msg.startswith( "die" ):
			if user == self.factory.owner:
				self.doQuit( user )
			else:
				return "F#$% off."

		elif msg.startswith( "part" ):
			if user == self.factory.owner:
				channels = msg.split( " " )[1:]

				for chan in channels:
					self.channels.remove( chan )
					self.leave( chan )

				self.SaveChannels()
			else:
				return "F#$% off."
	
		elif msg.startswith( "join" ):
			if user == self.factory.owner:
				channels = msg.split( " " )[1:]
				for chan in channels:
					self.channels.append( chan )
					self.join( chan )

				self.SaveChannels()
			else:
				return "F#$% off."
		else:
			return ""

	def doQuit( self, user ):
		self.factory.isQuitting = True
		self.quit( "Disconnected by %s" % ( user, ) )
		self.saveBlacklist()

	def SaveChannels( self ):
		channelString = ",".join( self.channels )
		config.set( "IRC", "channels", channelString )

		with open( "bot.config", "wb" ) as configfile:
			config.write( configfile )


class redbotFactory( protocol.ClientFactory ):
	protocol = redbot
	isQuitting = False

	def __init__( self, config ):
		self.nickname = config.get( "IRC", "nickname" )

		self.source_url = config.get( "General", "source_url" )
		self.owner = config.get( "General", "owner" )

		self.config = config
	
	def clientConnectionLost( self, connector, reason ):
		if not self.isQuitting:
			print( "Lost connection: " + str( reason ) )
			print( "Reconnecting..." )
			connector.connect()
		else:
			print( "Client exiting..." )
			reactor.stop()

	def clientConnectionFailed(self, connector, reason):
		print( "Could not connect: " + str( reason ) )

if __name__ == "__main__":
	config = ConfigParser.ConfigParser()
	config.read( "redbot.config" )

	server = config.get( "IRC", "server" )
	port = config.getint( "IRC", "port" )
		
	reactor.connectTCP( server, port, redbotFactory( config ) )
	reactor.run()
