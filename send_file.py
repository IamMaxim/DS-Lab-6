import socket
import sys
import os

HOST, PORT = sys.argv[-2], int(sys.argv[-1])
filenames = sys.argv[1:-2]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    # Send amount of files
    sock.sendall(len(filenames).to_bytes(4, 'big'))

    for filename in filenames:

        # Send the filename
        sock.sendall(len(filename).to_bytes(4, 'big'))
        sock.sendall(bytes(filename, "utf-8"))

        f = open(filename, 'rb')
        filesize = os.stat(filename).st_size

        # Send the file contents
        sock.sendall(filesize.to_bytes(4, 'big'))
        sent = 0
        while True:
            print('\rSent %i out of %i bytes (%i%%) of file %s    ' % (sent, filesize, 100 * sent / filesize, filename), end='')
            b = f.read(1024)
            sock.sendall(b)
            sent += len(b)
            if b == b'':
                break
        print('\rFile %s sent                                    ' % filename)
        f.close()

    sock.close()
