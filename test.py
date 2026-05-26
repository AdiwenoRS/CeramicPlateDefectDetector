from pwn import *

host = "127.0.0.1"
port = 80
io = remote(host, port)

