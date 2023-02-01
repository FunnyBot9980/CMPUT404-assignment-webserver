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
    
    response = ""
    
    codes = {
        'Ok': 200,
        'Moved Permanently': 301,
        'Bad Request': 400,
        'Not Found': 404,
        'Method Not Allowed': 405
    }
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        method, path = self.parse_request_data(self.data)
        # print(method)
        # print(path)
       
        if not self.valid_method(method):
            self.header_handler('Method Not Allowed')
            self.response += f"\r\n"
            self.send_response()
            return
        
        if path[-1] == '/':
            path += 'index.html'
         
        if method == 'GET':
            self.for_get(path)
            
        self.send_response()
        
    
    
    def for_get(self, path):
        root = './www'
        full_path = root + path
        
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                contents = f.read()
            
            self.header_handler('Ok')
            if full_path.endswith(".html"):
                self.response += "Content-Type: text/html\r\n"
            elif full_path.endswith(".css"):
                self.response += "Content-Type: text/css\r\n"
            self.response += f"\r\n"
            self.response += contents    
        else:
            self.header_handler('Not Found')
            self.response += f"\r\n"
        
    
    
    def valid_method(self, method):
        if method == 'GET':
            return True
        else:
            return False
        
          
    def parse_request_data(self, request_data):
        request_line, headers = request_data.split(b'\r\n', 1)
        method, path, http_version = request_line.decode('utf-8').split(" ")
        return (method, path)
    
    
    def header_handler(self, code):
        self.response = f"HTTP/1.1 {self.codes[code]} {code}\r\n"
        
        
    def send_response(self):
        self.request.sendall(bytearray(self.response, 'utf-8'))
        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
