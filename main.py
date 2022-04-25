import socket
import os
import sys
from ping import ping

MAX_TTL = 30
MAX_TIMEOUT = 5

def get_icmp_socket():
    icmp_proto = socket.getprotobyname("icmp")
    try:
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
        return icmp_socket
    except Exception as exc:
        print("Error! ", exc)

def main():
    ttl, pkg_id = 1,1

    while(ttl < MAX_TTL):
        icmp_socket = get_icmp_socket()
        host = sys.argv[1]
        ping_result = ping(host, icmp_socket, ttl, pkg_id, MAX_TIMEOUT)
        if ping_result:
            icmp_socket.close()
            break
        ttl += 1
        pkg_id += 1
        icmp_socket.close()
    os._exit(0)

main()
