#  coding: utf-8 
import socketserver
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

# http method to account for: GET, PUT, POST, OPTIONS, HEAD, DELETE
# https response codes: OK - 200, MOVED - 301, BAD REQUEST - 400, NOT_FOUND - 404, METHOD NOT ALLOWED - 405

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        method, path = self.parse_request_data(self.data)
        # print(method)
        # print(path)
       
        # check if valid method (hardcoded for now) 
        if not self.valid_method(method):
            response = b"HTTP/1.1 405 Method Not Allowed\r\n"
            self.request.sendall(response)
            return
        
        if path[-1] == '/':
            path += 'index.html'
         
        if method == 'GET':
            response = self.for_get(path)
            
        if response != None:  
            self.request.sendall(response)
        
    
    
    
    def for_get(self, path):
        root = './www'
        full_path = root + path
        
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                contents = f.read()
            
            response = b"HTTP/1.1 200 OK\r\n"
            if full_path.endswith(".html"):
                response += b"Content-Type: text/html\r\n"
            elif full_path.endswith(".css"):
                response += b"Content-Type: text/css\r\n"
            response += b"\r\n"
            response += contents 
            return response   
        else:
            return b"HTTP/1.1 404 Not Found\r\n\r\n"
        
    
    
    def valid_method(self, method):
        if method == 'GET':
            return True
        else:
            return False
        
        
        
    def parse_request_data(self, request_data):
        request_line, headers = request_data.split(b'\r\n', 1)
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
