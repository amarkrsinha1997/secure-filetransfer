import socket
from config import config

#globals

ips_ng_share = []


def connect_with_ip(ip, port=config.port):
    # print(ip)
    try:    
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(0.5)
        server_address = (ip, port)
        my_socket.connect(server_address)
    except Exception as e:
        pass
    else:
        ips_ng_share.append(ip)
    finally:
        my_socket.close()

def break_ip(ip):
    parts_4 = ip.split('.')
    return ".".join(parts_4[:3]), parts_4[3]

def get_all_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    my_ip = s.getsockname()[0]
    s.close()
    del s
    network_part, my_part = break_ip(my_ip)
    for x in range(1,255):
        if x == my_part:
            continue
        connect_with_ip(network_part + "." + str(x))
    return ips_ng_share
    
# if __name__ == '__main__':
#     main()
#     print ips_ng_share