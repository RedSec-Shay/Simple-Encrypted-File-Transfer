import socket
import subprocess
import sys
import os
import base64
import struct
import pprint
import hashlib
import re
import time
from Crypto.Cipher import AES
from hashlib import md5
from Crypto import Random

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32
PADDING = '{'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
# 32 character secret key - change this if you want to be unique
secret = "Fj39@vF4@38&8dE@!)(*^+-pL;'dK3J2"    #32
#secret = "Fj39@vF4@38&8dE@" #16
cipher = AES.new(secret)



if (len(sys.argv) < 2) or ('-h' in sys.argv) :
	print "Usage: Server - send_enc2.py -l <port>"
	print "       Client - send_enc2.py <server ip> <local file>  <port>"
	print "       Check md5hash - send_enc8.py md5 <file name>"
	sys.exit()
	

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
	data = ''
	while len(data) < n:
		packet = sock.recv(n - len(data))
		if not packet:
			return None
		data += packet
	return data
'''
def send_msg(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_msg(sock):
    lengthbuf = recvall(sock, 4)
    length = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
'''
def send_data(l):
	l = EncodeAES(cipher,l)	
	normal_size = len(l)
	normal_size = str(normal_size)
	normal_size_crypt= EncodeAES(cipher, normal_size)
	print normal_size
	s.sendall(normal_size_crypt)
	time.sleep(0.5)
	msglen=0
	#while  msglen < normal_size:
	for data in l:
		s.sendall(data)
		msglen = msglen + len (data)
		
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()	
	

if sys.argv[1] == "md5":
	print md5Checksum(sys.argv[2])
	sys.exit()
	
if sys.argv[1] == "-l":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("0.0.0.0",int(sys.argv[2])))
	s.listen(5) 
	while True:
		sc, address = s.accept()
		print address
		l = recv_msg(sc)
		pprint.pprint(l)
		r_split = re.split("\(\*\)", l)    #Split pathname and actual file contents
		pprint.pprint(r_split[0]);
		outfile = DecodeAES(cipher,r_split[0])
		print outfile
		l = DecodeAES(cipher,r_split[0])
		f = open(outfile,'wb') #open in binarya
		#l=sc.recv(1024)
		#print l
		#size = DecodeAES(cipher,l)
		#size = int(size)
		#print size
		#msglen=0
		#data=''
		#while msglen !=size:
		while True:		
					l=sc.recv(33554432)
					#l = recv_msg(sc)
					if  (l == ''):
						#print "No Data , exit.."
						break
					#data += l
					#msglen = msglen + len(l)
					#print msglen
					#l = DecodeAES(cipher,l)
					f.write(l)
					#if msglen >= size:break
		print "Got all , dycrypting.."			
		#l = DecodeAES(cipher,data)
		#print "Saving to File ..."
		#f.write(l)
		print "Done!"
		f.close()
		sc.close()
		
	
	
else:	
	host = sys.argv[1]
	filename = sys.argv[2]
	port = int(sys.argv[3])
	size = os.path.getsize(filename)
	s = socket.socket()
	s.connect((host,port))
	f=open (filename, "rb") 
	filename = EncodeAES(cipher,filename)
	l = (filename + "(*)")
	send_msg(s,l)
	time.sleep(0.5)
	sent = 0
	while True:
	#l=''
	#for data in f:
	#		l+=data
		l = f.read(33554432)
		if not l:
			break  # EOF
		#print "sending data..."
		#l = EncodeAES(cipher,l)
		sent = sent + len(l)
		print sent
		s.sendall(l)
		#send_msg(s,l)
		#send_data(l)
	print "exiting..."		
	s.close()   