import socket

sock = socket.socket()
# avoids the common address in use error when restarting:
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8000
sock.bind(("", port))
sock.listen()

print("listening on port", port, "...")

while True:
    (conn, addr) = sock.accept()
    print("new conn! from:", addr)

    req = conn.recv(4096)

    print("req recved:")
    print(req.decode())

    # read req and figure out what its asking for

    body = "I'm a server that sends actual http msgs! and you're a client!".encode()
    hdr = "HTTP/1.1 200 OK\r\ncontent-length: "
    hdr += str(len(body)) + "\r\n\r\n"
    hdr = hdr.encode()
    resp = hdr + body

    conn.sendall(resp)
    conn.close()
