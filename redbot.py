#! /usr/bin/env python3

import configparser
import praw
import traceback
import socket
import time
import threading
import socket
import imp
import glob
import sqlite3

from queue import Queue

class RedBot:
	send_queue = Queue()
	recv_queue = Queue()
	connected = False
	running = False
	commands = {}
	
	def __init__( self ):
		config = configparser.ConfigParser()
		config.read( "redbot.config" )

		self.channels = config.get( "IRC", "channels" )
		self.nickname = config.get( "IRC", "nickname" )
		self.server = config.get( "IRC", "server" )
		self.port = int( config.get( "IRC", "port" ) )
		self.commandPrefix = config.get( "IRC", "command_prefix" )
		self.owner = config.get( "General", "owner" )

		self.r = praw.Reddit( user_agent=config.get( "Reddit", "useragent" ) )
		self.r.login( config.get( "Reddit", "username" ), config.get( "Reddit", "password" ) )

		self.db = sqlite3.connect( "redbot.db" )

		self.socket = socket.socket()
		self.LoadCommands()

	def Run( self ):
		self.running = True
		
		self.Connect()

		self.recv_thread = threading.Thread( target=self.Listen )
		self.recv_thread.start()

		self.send_thread = threading.Thread( target=self.ProcessSendQueue )
		self.send_thread.start()

		while self.running:
			self.CheckForMessages()
			time.sleep( 0.1 )

	def Connect( self ):
		self.connected = False

		try:
			self.socket.connect( ( self.server, self.port ) )
		
			self.socket.send( bytes( "NICK %s\r\n" % ( self.nickname, ), 'UTF-8' ) )
			self.socket.send( bytes( "USER %s %s PB :%s\r\n" % ( self.nickname, self.nickname, self.nickname ), 'UTF-8' ) )

			for channel in self.channels.split( "," ):
				self.Join( channel )

			self.connected = True
		except:
			self.connected = False
			print( "Connect to %s on port %s failed.\n" % ( self.server, self.port ) )
			print( traceback.format_exc() )
			return
			
	def Listen( self ):
		while self.running:
			while not self.connected:
				self.Connect()

			data = self.socket.recv( 4096 )
			
			if len( data ) == 0:
				print( "Connection to %s lost. Attempting to reconnect...\n" % ( self.server, ) )
				self.connected = False
				continue

			data = data.decode( "UTF-8" )
			data = data.rstrip()
			line = data.split()

			if len( line ) < 1:
				continue
	
			if line[0] == "PING":
				self.SendRaw( "PONG " + line[1] )
			elif len( line ) > 2:
				if line[1] == 'PRIVMSG':
					msg_from = line[0].split('!')[0].lstrip(':')
					msg_to = line[2]
					msg = " ".join(line[3:]).lstrip(':')
					
					if msg_to == self.nickname:
						channel = msg_from
					else:
						channel = msg_to

					self.recv_queue.put( ( "MSG", msg_from, channel, msg ) )

				elif line[1] == 'JOIN':
					msg_from = line[0].split('!')[0].lstrip(':')
					channel = line[2]

					self.recv_queue.put( ( "ENTER", msg_from, channel ) )

				elif line[1] == 'PART':
					msg_from = line[0].split('!')[0].lstrip(':')
					channel = line[2]

					self.recv_queue.put( ( "LEAVE", msg_from, channel ) )

				elif line[1] == 'QUIT':
					msg_from = line[0].split('!')[0].lstrip(':')

					self.recv_queue.put( ( "QUIT", msg_from ) )

				elif line[1] == 'NICK':
					old_nick = line[0].split('!')[0].lstrip(':')
					new_nick = line[2].lstrip(':')

					self.recv_queue.put( ( "NICK", old_nick, new_nick ) )

	def Join( self, channel ):
		self.socket.send( bytes( "JOIN %s\r\n" % ( channel, ), 'UTF-8' ) )

	def Part( self, channel ):
		self.socket.send( bytes( "PART %s\r\n" % ( channel, ), 'UTF-8' ) )

	def SendText( self, channel, text ):
		msg = "PRIVMSG %s :%s\r\n" % ( channel, text )
		self.send_queue.put( msg )

	def SendAction( self, channel, text ):
		msg = "PRIVMSG %s :\001ACTION %s\001\r\n" % ( channel, text )
		self.send_queue.put( msg )
	
	def SendRaw( self, text ):
		msg = "%s\r\n" % ( text, )
		self.send_queue.put( msg )
		
	def Poll( self ):
		if self.recv_queue.empty():
			return None

		return self.recv_queue.get()

	def ProcessSendQueue( self ):
		while self.running:
			if self.connected and not self.send_queue.empty():
				self.socket.send( bytes( self.send_queue.get(), 'UTF-8' ) )
				self.send_queue.task_done()
			
			time.sleep( 0.5 ) 
			
	def Disconnect( self ):
		self.running = False
		self.connected = False
		self.socket.close()
		self.send_thread.join()
		self.recv_thread.join()
	
	def CheckForMessages( self ):
		msg = self.Poll()

		if msg and msg[0] == "MSG":
			nick = msg[1]
			channel = msg[2]
			msg = msg[3]

			if msg.startswith( self.commandPrefix ):
				self.HandleCommand( nick, channel, msg[1:] )
			elif msg.startswith( self.nickname ):
				self.HandleCommand( nick, channel, " ".join( msg.split( " " )[1:] ) )

	def LoadCommands( self ):
		self.commands.clear()
		files = glob.glob( "commands/*.py" )

		for path in files:
			name = path.partition( "/" )[2].rpartition( "." )[0]
			self.commands[ name ] = imp.load_source( name, path )

	def HandleCommand( self, nick, channel, cmd ):
		reply = None

		try:
			if cmd.startswith( "reload" ):
				self.LoadCommands()
				self.SendText( channel, "%s: Loaded %d commands: %s" % ( nick, len( self.commands ), ", ".join( self.commands.keys() ) ) )
			else:
				for command, module in self.commands.items():
					if cmd.startswith( command ):
						module.Run( self, nick, channel, cmd )
						return

				self.SendText( channel, "%s: Unknown command." % ( nick, ) )
						
		except:
			print( traceback.format_exc() )
			self.SendText( channel, "%s: Error processing request." % ( nick, ) )


def main():
	bot = RedBot()
	bot.Run()

if __name__ == "__main__":
	main()

