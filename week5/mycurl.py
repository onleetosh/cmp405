import socket
import sys

# sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock = socket.socket()

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    print("usage: python3 mycurl.py URL")
    sys.exit()

port = 80
sock.connect((host, port))

req = "GET / HTTP/1.1\r\n"
req += "host: " + host + "\r\n"
req += "connection: close\r\n"
req += "\r\n"

sock.sendall(req.encode())

# resp = sock.recv(300)
resp = b""
found_crnl = False
body_bytes = 0
while more := sock.recv(51):
    resp += more
    # are we at the end of the header yet??
    i = resp.find(b"\r\n\r\n")
    if not found_crnl and i >= 0:
        found_crnl = True
        print("found it!")
    if found_crnl:
        body_bytes += len(more)
        # print("more:", more + b"end")
        print(b"**len(" + more + b"):", len(more))
        # print("more dec:", more.decode() + "end")
        print("len more dec:", len(more.decode()))
        print()
        print()

print("total len:", len(resp))

# resp = b""
# more = sock.recv(300)
# while more != "":
#     resp += more
#     more = sock.recv(300)


resp = resp.decode()

head, body = resp.split("\r\n\r\n", 1)

# print(head)

# print(resp)
# want:
# print(body)
