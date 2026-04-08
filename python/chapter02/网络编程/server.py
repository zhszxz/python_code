"""
服务器端
"""

import socket

# 1.创建服务器socket, 参数: AF_INET: ipv4, SOCK_STREAM: tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2.绑定ip和端口
server_socket.bind(("", 8080))
# 3.监听端口, 参数: 最大连接数
server_socket.listen(5)
# 4.等待客户端连接
accept_socket, client_info = server_socket.accept()
print(f"客户端已连接: {client_info}")
# 5.发送数据
accept_socket.send(b"hello, client")
# 5.接收数据
data = accept_socket.recv(1024).decode("utf-8")
print(f"接收到数据: {data}")
# 6.关闭连接
accept_socket.close()
