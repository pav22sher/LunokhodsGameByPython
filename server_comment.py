#импортируем библиотеки
import socket
import json
from random import *

#функция определяет проиграл ли первый игрок
def gameOver1(state):
	for r in range(8):
		for c in range(8):
			if state[r][c]==1:
				return False #первый игрок проиграл
	else: return True #первый игрок НЕ проиграл
#тоже самое для второго игрока
def gameOver2(state):
	for r in range(8):
		for c in range(8):
			if state[r][c]==2:
				return False
	else: return True
#переворачиваем игровую доску для второго игрока
def flip(a):
	b=[[0 for i in range(8)] for j in range(8)]
	for i in range(8):
		for j in range(8):
			b[i][j]=a[abs(i-7)][abs(j-7)]
	return b
#инициализация игровой доски(расположение игроков и препятствий на доске)
#двумерный лист-игровая доска, первый игрок-1, второй игрок-2
#препятствие-3, пустое поле-0 
def state_init(state):
	for r in range(8):
		for c in range(8):
			if r==r_play2 and c==c_play2:
				state[r][c]=2
			elif r==r_play1 and c==c_play1:
				state[r][c]=1
			elif (r>0 and r<7) and randint(0, 1)==1:
				state[r][c]=3
			else:
				state[r][c]=0

#JSON (англ. JavaScript Object Notation)
#json.dumps-сериализует объект Python в строку JSON-формата.
#json.loads-десериализует строку JSON-формата в объект Python.
#Сериализация — процесс перевода объекта Python
#в последовательность(серию) битов(байтов).
				
PORT = 2222#системные (0—1023), пользовательские (1024—49151) и частные (49152—65535)

#string.encode('<название кодировки>') # переводим строку в байтовую строку
#b'<байт-строка>'.decode('<название кодировки>') # переводим байтовую строку в строку
json_start=json.dumps("start")
json_stop=json.dumps("stop")
json_lose=json.dumps("Вы проиграли!")
json_win=json.dumps("Вы победили!")

#Метод socket создает сокет
#Оператор with используется для автоматического закрытия сокета в конце блока.
#domain указывающий семейство протоколов сокета: AF_INET для сетевого протокола IPv4
#type SOCK_STREAM (надёжная потокоориентированная служба или потоковый сокет(TCP))
#protocol=0 (протокол не указан) используется значение по умолчанию для данного вида соединений.
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)

#Метод bind свяжет сокет с хостом(IP-адресом) и портом 
#Если указать "127.0.0.1", то подключиться можно будет только с этого же компьютера.
#Если не указать хост или указать "0.0.0.0", сокет будет прослушивать все хосты
server.bind(("localhost", PORT))

#Метод listen запускает режим прослушивания для сокета. 
#Метод принимает один аргумент — максимальное количество подключений в очереди.
server.listen(2)

#Метод accept примет подключение и вернет сокет и адрес клиента
print ("Ожидаем подключения игроков...")
conn1, adr1 = server.accept()
print ("Первый игрок подключился...")
conn2, adr2 = server.accept()
print ("Второй игрок подключился...")

#игровая доска инициализируется нулями
state=[[0 for c in range(8)] for r in range(8)]
#случайным образом задаем начальные позиции игроков
c_play1=randint(0, 7)
r_play1=7
c_play2=randint(0, 7)
r_play2=0
#инициализация игровой доски
state_init(state)
win_num=0#номер игрока, который выиграл

try:
	conn1.send(json.dumps(1).encode())#1 игрок узнает свой номер
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(2).encode())#и номер противника
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(state).encode())#посылаем игровую доску 1 игроку
	json.loads(conn1.recv(1024).decode())
	
	conn2.send(json.dumps(2).encode())#2 игрок узнает свой номер
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(1).encode())#и номер противника
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(flip(state)).encode())#посылаем игровую доску 2 игроку
	json.loads(conn2.recv(1024).decode())
	
	while True:#бесконечный цикл работы с игроками
		conn1.send(json.dumps("Start").encode())#метка старта 1 игрока
		#принимаем сообщение что все хорошо(для синхронизациии(костыль))
		json.loads(conn1.recv(1024).decode())
		#посылаем актуальную игровую доску
		conn1.send(json.dumps(state).encode())
		#принимаем измененную игроком доску
		state = json.loads(conn1.recv(1024).decode())
		if gameOver2(state):#если второй игрок проиграл
			win_num=1#то первый выигрыл
			break#выход из бесконечного цыкла
		
		conn2.send(json.dumps("Start").encode())#метка старта 2 игрока
		#принимаем сообщение что все хорошо(для синхронизациии(костыль))
		json.loads(conn2.recv(1024).decode())
		#посылаем актуальную игровую доску
		conn2.send(json.dumps(flip(state)).encode())
		#принимаем измененную игроком доску
		state = flip(json.loads(conn2.recv(1024).decode()))
		if gameOver1(state):#если первый игрок проиграл
			win_num=2#то второй игрок выигрыл
			break#выход из бесконечного цыкла
	
	#Отправляем сообщение о том кто выйигрыл, а кто проиграл
	if win_num==1:
		conn1.send(json_win.encode())
		conn2.send(json_lose.encode())
	else:
		conn1.send(json_lose.encode())
		conn2.send(json_win.encode())
	
	#Посылаем коненчое состояние доски обоим игрокам
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(state).encode())
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(flip(state)).encode())
		
	print("Игра закончилась!")	
		
except BaseException:#ловим все возможные исключения
	print("Ошибка!!!")
#Метод close закрывает сокет.	
conn1.close()
conn2.close()
server.close()