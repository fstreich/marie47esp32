from marie47esp32.util.log import log
import socket

'''
	UDP paket:
		0 : 'FS'		- magic number
		2 : (x)			- installation id
		3 : (cmd)		- command
		{4... : (parameter) }
		
		cmd: 0 - ping
		
		cmd: 1 - pong
		
		cmd: 3 - error
			par: msg

'''
class UdpServer(object):
	
	clients = []

	def update_client(udpdata,addr):
		pass
	def handle_udp_paket(udpdata, addr, sock):
		
		if len(udpdata)<4:
			log.error("udpserver: upd mesg too short! from: "+str(addr))
			sock.sendto(b'\x46\x53\x00\x03message too short\n', addr)
			return
		if (udpdata[0] != 70) or (udpdata[1] != 83):
			log.error("udpserver: udp magic error! "+str(udpdata[0])+str(udpdata[1])+" from: "+str(addr))
			sock.sendto(b'\x46\x53\x00\x03magic error\n', addr)
			return
		log.debug('udpserver: received: '+str(udpdata)+" from: "+str(addr))
		
		# ping
		if udpdata[3] == 0:
			log.debug("udpserver: ping received: from: "+str(addr))
			data = bytearray(b'\x46\x53\x00\x01')
			data[2] = udpdata[2]
			sock.sendto(data, addr)
			UdpServer.update_client(udpdata,addr)
			
		else:
			log.debug("udpserver: unknown command: "+str(udpdata[3])+" from: "+str(addr))
			sock.sendto(b'\x46\x53\x00\x03wrong command\n', addr)
        
	def send_to_clients(msg):
		pass
 
 
 