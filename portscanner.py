#!/usr/bin/python3.8

import socket
import sys


if len(sys.argv) != 4:
    print("Usage:\r\n"
          "./portscanner.py <target IP> [single | range | list] [<port number> | <port range> | <file name>]\r\n"
          "\r\n"
          "Examples:\r\n"
          "./portscanner.py 192.168.0.10 single 443\r\n"
          "./portscanner.py 192.168.0.10 list port_list.txt\r\n"
          "./portscanner.py 192.168.0.10 range 1,65535\r\n"
          "\r\n")
    exit()

target = str(sys.argv[1])
portformat = str(sys.argv[2])

if portformat == "single":
    portvalue = int(sys.argv[3])
    port = portvalue
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = client_sock.connect_ex((target,port))
    if result == 0:
        print("Port", port, "is open!")
        banner = client_sock.recv(128)
        print("Port", port, "banner:", banner)
    client_sock.close()

if portformat == "range":
    portvalue = (str(sys.argv[3])).split(",")
    for port in range(int(portvalue[0]), int(portvalue[1])+1):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client_sock.connect_ex((target, port))
        if result == 0:
            print("Port", port, "is open!")
            banner = client_sock.recv(128)
            print("Port", port, "banner:", banner)
        client_sock.close()

if portformat == "list":
    filename = str(sys.argv[3])
    file = open(filename, "r")
    portvalue = list((file.read()).split("\n"))[:-1]
    file.close()
    for port in portvalue:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client_sock.connect_ex((target, int(port)))
        client_sock.settimeout(3)
        if result == 0:
            print("Port", port, "is open!")
            banner = client_sock.recv(128)
            if banner:
                print("Port", port, "banner:", banner)
            elif not banner:
                print("No banner found, service is not FTP/SSH/Telnet/SMTP.")
        client_sock.close()

print("\r\n"
      "Port scan has completed, any open ports/banners are displayed.")
