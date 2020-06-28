from marie47esp32.util.log import log
import socket
import datetime

'''
	UDP paket:
		0 : 'F'		- magic number
		1 : 'S'		- magic number
		2 :  0x01		- installation type
		3 : (x)			- installation id
		4 : (cmd)		- command
		{5... : (parameter) }
		
		cmd: 0 - ping
		
		cmd: 1 - pong
		
		cmd: 3 - error
			par: msg
		
		cmd: 4 - play now
			par: program
'''
from datetime import date, datetime

class UdpClient(object):
	
	clients = []
	
	def __init__(self, addr, type, id):
		self.addr = addr
		self.type = type
		self.id = id
		self.lastseen = datetime.now()
		
	def sendto(self, msg):
		log.debug("udpclient: send to client: "+str(self.addr)+" msg: "+str(msg))
		UdpServer.sock.sendto(msg, self.addr)
		
	## to set client from config
	def update_client_from_string(addrstring, type, id):
		UdpClient.update_client(socket.inet_aton(addr), type, id)
		
	def update_client(addr, type, id):
		client = None
		## already in list?
		for c in UdpClient.clients:
			if c.type == type and c.id == id:
				client = c
				if c.addr[0]!=addr[0] and c.addr[1]!=addr[1]:
					log.debug("UdpClient: ip of client changed: old: "+str(c.addr)+" new: "+str(addr))
					c.addr = addr
					log.debug("UdpClient: ip of client changed")
				else:
					log.debug("UdpClient: client already known...: "+str(c.addr))
				break
		## new client
		if client is None:
			client = UdpClient(addr, type, id)
			UdpClient.clients.append(client)
			log.debug("UdpClient: new client: "+str(addr)+" clients: "+str(len(UdpClient.clients)))
		client.lastseen = datetime.now()
		return client
		
	def sendto_clients(id, data):
		client = None
		for c in UdpClient.clients:
			if c.id == id:
				client = c
				c.sendto(data)
		return client
	
class UdpServer(object):
	
	sock = None

	def handle_udp_paket(udpdata, addr):
		
		if len(udpdata)<4:
			log.error("udpserver: upd mesg too short! from: "+str(addr))
			UdpServer.sock.sendto(b'\x46\x53\x00\x03message too short\n', addr)
			return
		if (udpdata[0] != 70) or (udpdata[1] != 83):
			log.error("udpserver: udp magic error! "+str(udpdata[0])+str(udpdata[1])+" from: "+str(addr))
			UdpServer.sock.sendto(b'\x46\x53\x00\x03magic error\n', addr)
			return
		
		client = UdpClient.update_client(addr, type=udpdata[2], id=udpdata[3])
		
		if (udpdata[2] != 1):
			log.error("udpserver: unknown installation type! "+str(udpdata[2])+" from: "+str(addr))
			client.sendto(b'\x46\x53\x00\x03unknown installation\n')
			return
		
		log.debug('udpserver: received: '+str(udpdata)+" from: "+str(client.addr))
		
		# ping
		if udpdata[4] == 0:
			log.debug("udpserver: ping received: from: "+str(addr))
			data = bytearray(b'\x46\x53\x00\x00\x01')
			data[2] = udpdata[2]
			data[3] = udpdata[3]
			client.sendto(data)
		else:
			log.debug("udpserver: unknown command: "+str(udpdata[4])+" from: "+str(addr))
			client.sendto(b'\x46\x53\x00\x03wrong command\n', addr)
	
	def setEditMode(program):
		log.debug('udpserver: setEditMode')
		data = bytearray(b'\x46\x53\x00\x00\x04')
		data.extend(program.getUDPbytes())
		UdpClient.sendto_clients(1, data)
		pass
	def endEditMode():
		log.debug('udpserver: endEditMode')
		pass

 