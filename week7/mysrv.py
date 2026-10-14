import socket

sock = socket.socket()
# avoids the common address in use error when restarting:
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8000

sock.bind(('', port))
sock.listen() 
print("log: listening on port", port, "...")

while True:
    (conn, addr) = sock.accept() 
    print('new conn! from:', addr)

    col = ''
    req = conn.recv(4096).decode()

    lines = req.split('\r\n')
    firstline = lines[0]
    middle = firstline.split(' ')[1]
    if middle == '/favicon.ico':
        print('death to favicons!')
        continue

    print("log: request recieved")
    print(req)

    for line in lines:
        if line.lower().startswith('cookie: '):
            cookline = line
            rest = line[len('cookie: '):]
            cooks = rest.split('; ')
            for cook in cooks:
                k,v = cook.split('=')
                print("log: cookie param", k, "=", v, "!")
                if k == "color":
                    col = v
    print("log: firstline:", firstline)
    print("log: middle:", middle)
    qloc = middle.find("?")
    if qloc > - 1:
        cookiestr = middle[qloc + 1 :]
        print("log: cookiestr:", cookiestr)
        keyvalstrs = cookiestr.split('&')
        for kvstr in keyvalstrs:
            k,v = kvstr.split('=')
            print("log: get param", k, "=", v, "!")
            if k == "color":
                col = v
                print("log: I think i found the color cookie val!!:")
                print(col)

    body = f""" <html>
            <head></head>
            <body bgcolor={col}>
                 I'm a server that sends actual http msgs--containing 
            <b><i>actual html !!</i></b>
            <p>
            <form target='' method="get">
            flavor:
            <input type=text name='flavor'><br>
            color:
            <input type=text name='color'><br>
            size:
            <input type=text name='size'><br>
            <input type=submit name='btn' value='click me!'><br>
            </form>
            </body>
            </html>""".encode()
    hdr = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\ncontent-length:"
    hdr += str(len(body)) + "\r\n\r\n"
    print("log: hdr")
    print(hdr)

    hdr = hdr.encode()
    resp = hdr + body
    # read req and figure out what its asking for 
    #resp = "I'm a server and you're the client!"
    conn.sendall(resp)
    conn.close()