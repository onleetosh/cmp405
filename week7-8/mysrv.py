import socket
import random

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

    #conn 
    col = ""

    req = conn.recv(4096).decode()

    
    req = ''
    while True:
        more = conn.recv(5) #tries to read the request 5 bytes at a time
        if more:
            req += more
        else:
            break
            
    lines = req.split("\r\n")
    firstline = lines[0]
    middle = firstline.split(" ")[1]
    method = firstline.split(" ")[0]

    if middle == "/favicon.ico":
        print("death to favicons!")
        continue

    print("req recved:")
    print(req)

    cooks = {}
    for line in lines:
        if line.lower().startswith("cookie: "):
            cookline = line
            rest = line[len("cookie: ") :]
            cookstr = rest.split("; ")
            for cook in cookstr:
                k, v = cook.split("=")
                if k == "color":
                    col = v
                    print("i think i found the color cookie val!!:", col)
                    # building a key value table example:
                    # d = {}
                    # d['x'] = 10
                    # d['rr'] = 20

    # 10-21 addition                 
    if 'color' in cooks:
        col = cooks['color']                  # inserts an entry into the hash table 'dictionary'

        print("found the color cookie", col)
        
    print("AFTER COOKIE S4ACH")

    print("firstline:", firstline)
    print("middle:", middle)
    qloc = middle.find("?")
    print("qloc:", qloc)
    if method == "GET" and qloc > -1:
        paramstr = middle[qloc + 1 :]
        print("*** found get params:", paramstr)
    elif method == "POST" and "Content-Length: ".lower() in req.lower():
        # paramstr = conn.recv(4096)
        paramstr = req.split("\r\n\r\n")[1]
        print("*** found POST params:", paramstr)
    else:
        paramstr = ""
        print("** didn't find any params")

    params = {}

    #
    if paramstr:
        print("paramstr:", paramstr)
        keyvalstrs = paramstr.split("&")
        for kvstr in keyvalstrs:
            k, v = kvstr.split("=")
            print("get param", k, "=", v, "!")
            params[k] = v
            #if k == "color":
             #   col = v
              #  print("setting col to", v)
    if "color" in params:
        col = params['color']
        #print("setting col to", params['color'])
        print("setting col to", col)
    colors = "white\nred\ngreen\nblue\nyellow\norange\npurple\npink\ncyan\nmagenta\nlime\nteal\nnavy\nmaroon\nolive\naqua\nfuchsia\nsilver\ngray\nblack\nwhite\ngold\ncoral\nsalmon\nturquoise\nindigo\nviolet\nbrown\ntan\nkhaki\ncrimson\nplum\norchid\nlavender\nbeige\nchocolate"
    colors = colors.split("\n")

    # if col is random then write random to the cookie
    # but use a randomly chosen color in the page
    if col == "random":
        pagecol = colors[random.randrange(len(colors))]
    else:
        pagecol = col

    body = f"""<html>
    <head>
    <link rel="icon" href="https://www.google.com/favicon.ico">
    </head>
    <body bgcolor={pagecol}>
    I'm a server that sends actual http msg--containing 
    <b><i>actual html!!</i></b>
    <p>
    <form target='' method="post">
        flavor:
        <input type=text name='flavor'><br>
        color:
        <input type=text name='color'><br>
        size:
        <input type=text name='size'><br>
        <input type=submit name='btn' value='click me!'>
    </form>
    </body>
    </html>""".encode()

    hdr = "HTTP/1.1 200 OK\r\ncontent-type: text/html\r\ncontent-length: "
    hdr += str(len(body)) + "\r\n"
    hdr += "set-cookie: color=" + col + "\r\n"
    hdr += "set-cookie: somerenadomcookie=whatever" + "\r\n\r\n"

    print("RESPONSE:")
    print(hdr)

    hdr = hdr.encode()
    resp = hdr + body

    conn.sendall(resp)
    conn.close()
