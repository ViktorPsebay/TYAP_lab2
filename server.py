#SERVER
import random, pickle, threading, time
from socket import *


def matrixs_generation(size, matrix1, matrix2):
    for i in range(size):
        matrix1.append([])
        matrix2.append([])
    for item in matrix1:
        str_size = 0
        while str_size < size:
            element = random.randint(0, 10)
            item.append(element)
            str_size += 1
    for item in matrix2:
        str_size = 0
        while str_size < size:
            element = random.randint(0, 10)
            item.append(element)
            str_size += 1

    return matrix1, matrix2


def tasks(clients, matrix1, matrix2, current_elem):
    print("I'm working...")
    while True:
        LOCK.acquire()
        for client in clients.keys():
            if clients.get(client) == True:
                for elem in current_elem.keys():

                    if current_elem.get(elem) == True:
                        data = []
                        data.append(matrix1)
                        data.append(matrix2)
                        data.append(size)
                        data.append(elem)

                        try:
                            client.send(pickle.dumps(data))
                            current_elem.update({elem: False})
                            clients.update({client: False})



                        except socket.error:
                            print("Client was killed :'(")
                            clients.pop(client)

                        break
        LOCK.release()
        time.sleep(0.5)


def matrix3_consrtucntion(elements, size):
    nx = 0
    ny = 0

    for i in range(size):
        matrix3.append([])
    for item in matrix3:
        str_size = 0
        while str_size < size:
            item.append(0)
            str_size += 1

    for key in elements.keys():
        nx = int(key / size)
        ny = int(key % size)

        matrix3[nx][ny] = elements.get(key)

    for count in matrix3:
        print(count)


def listener():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 54545))
    server_socket = socket()
    server_socket.bind(('', 9021))
    print("I'm listening...")

    while True:
        data, addr1 = s.recvfrom(1024)
        print(data, addr1)
        s.sendto(b'I am srv', addr1)

        server_socket.listen(SOMAXCONN)
        conn, addr2 = server_socket.accept()

        print("accept new connection from", addr2)

        if conn not in clients.keys():
            LOCK.acquire()
            clients.update({conn: True})
            LOCK.release()


def receive(clients):
    print("I'm receiving")
    while True:
        LOCK.acquire()
        for client in clients.keys():
            data = client.recv(10000)
            data = pickle.loads(data)
            clients.update({client: True})
            res_elements.update(data)

            if len(res_elements) == size * size:
                print("")
                for q in matrix1:
                    print(q)
                print("")
                for x in matrix2:
                    print(x)
                print("")

                matrix3_consrtucntion(res_elements, size)

        LOCK.release()
        time.sleep(0.5)


size = input('Input size your matrix: ')
size = int(size)
current_elem = {}
for item in range(size * size):
    current_elem.update({item: True})
matrix1 = []
matrix2 = []
matrix3 = []
matrixs_generation(size, matrix1, matrix2)
res_elements = {}
clients = {}
LOCK = threading.Lock()

lstn = threading.Thread(target=listener, args=())
lstn.start()

time.sleep(10)
tsk = threading.Thread(target=tasks, args=(clients, matrix1, matrix2, current_elem))
tsk.start()

rcv = threading.Thread(target=receive, args=(clients,))
rcv.start()
