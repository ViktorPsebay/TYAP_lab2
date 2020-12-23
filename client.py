#CLIENT
import pickle, time
from socket import *

matrix3 = []
def matrix_worker(matrix1, matrix2, size, k):
    time.sleep(0.05)
    res = 0
    nx=int(k/size)
    ny=int(k%size)
    i=0
    while i<size:
        res+=matrix1[nx][i]*matrix2[i][ny]
        i+=1
    el = {k:res}
    print(el)
    data = pickle.dumps(el)
    client_socket.send(data)


cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

client_socket = socket()

cs.sendto(b'I am client', ('255.255.255.255', 54545))
data, addr = cs.recvfrom(10000000)
ip, port = addr
print(data,addr)
client_socket.connect((ip, 9021))

while True:
    data = client_socket.recv(10000000)



    data=pickle.loads(data)
    matrix1 = data[0]
    matrix2 = data[1]
    size = data[2]
    k = data[3]
    matrix_worker(matrix1, matrix2, size, k)

client_socket.close()
