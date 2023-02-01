#  coding: utf-8 
import socketserver
from email.parser import BytesParser
import os
# Copyright 2023 Abram Hindle, Eddie Antonio Santos, John Macdonald
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        method, path = self.parse_request_data(self.data)
       
        print(method)
        print(path)
        
        # f = open('index.html', 'rb')
        # contents = f.read()
        # f.close()
 
        # body = 
        
        # self.request.send(result.encode('utf-8'))

        # response = b"HTTP/1.1 200 OK\r\n"
        # response += b"Content-Type: text/html\r\n"
        # response += b"\r\n"
        # response += contents
        
        # self.request.sendall(response)
        self.request.sendall(bytearray("OK",'utf-8'))
        
    def parse_request_data(self, request_data):
        request_line, headers = request_data.split(b'\r\n', 1)
        # headers = BytesParser().parsebytes(headers)
        method, path, http_version = request_line.decode('utf-8').split(" ")
        
        return (method, path)
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
