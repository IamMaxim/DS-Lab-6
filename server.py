import socketserver
import os


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        file_count = int.from_bytes(self.request.recv(4), 'big')

        for i in range(file_count):
            filename_len = int.from_bytes(self.request.recv(4), 'big')
            filename = str(self.request.recv(filename_len), 'utf-8')

            print('Filename of length %i received: %s' % (filename_len, filename))

            filename = os.path.basename(filename)
            filename = 'received/' + filename
            if os.path.exists(filename):
                counter = 1
                while os.path.exists(filename + '_copy' + str(counter)):
                        counter += 1
                filename += '_copy' + str(counter)

            f = open(filename, 'wb+')

            filesize = int.from_bytes(self.request.recv(4), 'big')
            received = 0
            while True:
                data = self.request.recv(min(1024, filesize - received))
                if data == b'':
                    break
                f.write(data)
                received += len(data)
            f.close()


with socketserver.TCPServer(('0.0.0.0', 18528), MyTCPHandler) as server:
    server.serve_forever()
