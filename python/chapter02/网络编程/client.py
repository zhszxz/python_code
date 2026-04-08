"""
客户端
"""
import socket

# 1.创建客户端socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2.连接服务器
client_socket.connect(("127.0.0.1", 8080))
print("已连接服务器")
# 3.接收数据
data = client_socket.recv(1024).decode("utf-8")
print(f"接收到数据: {data}")
# 4.发送数据
client_socket.send("你好,套接字!".encode("utf-8"))
# 5.关闭连接
client_socket.close()
