#!/usr/bin/env python

import ssl
import pprint
import socket

CACerts = '/etc/pki/tls/cert.pem'  # Fedora
#CACerts = '/etc/ssl/certs/ca-certificates.crt'  # Debian

RemoteHost = 'www.verisign.com'
RemotePort = 443

# establish a connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RemoteHost, RemotePort))

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s, ca_certs=CACerts, cert_reqs=ssl.CERT_REQUIRED)

print 'PeerName:', repr(ssl_sock.getpeername())
print 'Cipher:', ssl_sock.cipher()
print 'PeerCert:', pprint.pformat(ssl_sock.getpeercert())

# Set a simple HTTP request
ssl_sock.write("""GET / HTTP/1.0\r\nHost: %s\r\n\r\n""" % RemoteHost)

# Read a chunk of data.
data = ssl_sock.read()
print data

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()
