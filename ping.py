import struct
import socket
import os
import select
import time
from checksum import get_checksum

ECHO_REQUEST_CODE = 8
ECHO_RESPONSE_CODE = 0
ICMP_SIZE = 1024

def print_timeout_exceeded(ttl, time_diff):
    print("Timeout exceeded. TTL: %s. %sms"%(str(ttl), str(time_diff)))

def print_hop_result(ttl, time_diff, hostname, addr):
    print("%s %s (%s) %s" % (str(ttl), str(addr), str(hostname), str(time_diff)))

def get_time_diff(time1, time2) -> float:
    return abs(float(time1 - time2))

def get_icmp_package(id):
    package = struct.pack('bbHHh', ECHO_REQUEST_CODE, ECHO_RESPONSE_CODE, 0, id, 1)
    checksum = get_checksum(package)
    package = struct.pack('bbHHh', ECHO_REQUEST_CODE, ECHO_RESPONSE_CODE, checksum, id,1)
    return package

def get_hostname(addr: str):
    result = 'Unknown host'
    try:
        host_info = socket.gethostbyaddr(addr)
        if host_info:
            result = host_info[0]
    except:
        pass
    return result

def ping(dest_host: str, icmp_socket, ttl:int, id:int, timeout: int):
    package = get_icmp_package(id)
    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    icmp_socket.sendto(package, (dest_host, 1))

    start_time = time.time()
    resp = select.select([icmp_socket], [], [], timeout)
    if not resp[0]:
        time_diff = get_time_diff(time.time(), start_time)
        print_timeout_exceeded(ttl, time_diff)
        return False

    recv_packet, addr = icmp_socket.recvfrom(ICMP_SIZE)
    hostname = get_hostname(addr[0])

    time_diff = get_time_diff(time.time(), start_time)
    print_hop_result(ttl, time_diff, addr[0], hostname)

    if addr[0] == dest_host:
        return True

    return False
