import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import sistema_pb2, sistema_pb2_grpc
import socket
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton('0.0.0.0')
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Monitorando Orquestrador Principal...")
while True:
    sock.settimeout(5)
    try:
        data, addr = sock.recvfrom(1024)
    except socket.timeout:
        print("!!! FALHA DETECTADA: Assumindo como Principal (Failover) !!!")
        break