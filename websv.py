#!python3.8
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import proc
import random
import string
import re
import psutil
import math
maintainancing = False
pages = ["start","stop","main","maintenance","success","error"]
pages_txt= {}
#load all pages
for page in pages:
    with open(f"websv/{page}.html",mode="r",encoding="utf-8") as f:
        txt = f.read()
    pages_txt[f"{page}.html"] = txt
    print(f"{page}.html")
def randomname(n):
     return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def passgenarate(sv_dir):
      path = f'{sv_dir}\server_config.xml'
      f = open(path, 'r', encoding='UTF-8')
      data = f.read()
      f.close()
      pw = randomname(8)
      new_data = re.sub('password="([A-Za-z0-9]+)"',f'password="{pw}"',data)
      with open(path, mode='w') as f:
            f.write(new_data)
      path_w = f'{sv_dir}\password.txt'
      with open(path_w, mode='w') as f:
            f.write(pw)
def process_check(sv_dir):
      path = os.getcwd() + f"\{sv_dir}\{sv_dir}_server.exe"
      print(path)
      return proc.process_find(path)
def passw():
    path =f'ssk/password.txt'
    with open(path) as f:
        s = f.read()
    return s
class S(BaseHTTPRequestHandler):
    def _set_headers(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        req = self.requestline[5:].split()[0]
        stat = process_check("ssk")
        if maintainancing:
            svt = pages_txt["maintenance.html"]
        elif req in pages_txt:
            svt = pages_txt[req]
        else:
            svt = pages_txt["main.html"]
        if req == "start_ok":
            if not stat:
                print("starting")
                try:
                    os.rename("ssk/server64.exe","ssk/ssk_server.exe")
                except:
                    pass
                passgenarate("ssk")
                os.system("ssk_subwindow.bat")
                svt = pages_txt["success.html"]
            else:
                svt = pages_txt["error.html"]
        elif req == "stop_ok":
            if stat:
                os.system(f"taskkill /t /f /im ssk_server.exe")
                svt = pages_txt["success.html"]
            else:
                svt = pages_txt["error.html"]
        pw = passw()
        svt = svt.replace("thisispassword",pw)
        cpu_persent= psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_persent= math.floor(mem.used / mem.total*1000)/10
        mem_total= math.floor(mem.total/1000000)
        mem_used= math.floor(mem.used/1000000)
        st = f"<p></p><h3>起動中:{str(stat)}</h3><p></p>CPU:{cpu_persent}%\n<p></p>RAM:{mem_persent}%({mem_used}/{mem_total}MB)"
        svt = svt.replace("thisisstatus",st)
        self._set_headers()
        self.wfile.write(svt.encode())
    
    def do_POST(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>POST message receive!</h1></body></html>".encode())

def run_http_server(server_class=HTTPServer, handler_class=S, port=8080):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()
def run():
    run_http_server(server_class=HTTPServer)
stat = process_check("ssk")
if __name__ == '__main__':
    run()