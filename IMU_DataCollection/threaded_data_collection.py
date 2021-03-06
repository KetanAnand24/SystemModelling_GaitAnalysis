import threading
from threading import Thread
import time
import socket
import datetime
from datetime import datetime
import signal

try:
    collect_time = int(input("Enter time in seconds to collect data\n"))
except:
    collect_time = 60
port1 = 9999
filename1 = input('Enter filename for sensor connected on port {}\n'.format(port1))
# exit_event1 = threading.Event()
port2 = 8888
filename2 = input('Enter filename for sensor connected on port {}\n'.format(port2))
# exit_event2 = threading.Event()
port3 = 7777
filename3 = input('Enter filename for sensor connected on port {}\n'.format(port3))
# exit_event3 = threading.Event()
port4 = 6666
filename4 = input('Enter filename for sensor connected on port {}\n'.format(port4))
# exit_event4 = threading.Event()
port5 = 5555
filename5 = input('Enter filename for sensor connected on port {}\n'.format(port5))
# exit_event4 = threading.Event()
port6 = 4444
filename6 = input('Enter filename for sensor connected on port {}\n'.format(port6))
# exit_event4 = threading.Event()
port7 = 3333
filename7 = input('Enter filename for sensor connected on port {}\n'.format(port7))
# exit_event4 = threading.Event()
class camThread(threading.Thread):
    def __init__(self, port, filename):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0",port))
        self.sock.setblocking(0)
        self.filename = filename
        self.lock = threading.Lock()
        self.exit_event = threading.Event()
        self.port = port
    def run(self):
        print("Starting on port", self.port)
        data_receive(self, self.filename, self.sock, self.lock, self.exit_event, self.port)


def data_receive(threadname, filename, sock, lock, exit_event, port):
    lock.acquire()
    count = 0
    rate = 0
    initial = 0
    with open(filename + '.csv', 'w') as fp:
        fp.write('AccX,AccY,AccZ,GyroX,GyroY,GyroZ,Q1, Q2, Q3, Q4, Yaw,Pitch,Roll,count,imu_time,receiver_time,DATA_RATE\n')
        # fp.write('count, time, rate\n')
        # print("{} has entered here at {}".format(threadname, datetime.now().time()))
        start = time.time()
        try:
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))    
            while time.time()-start<collect_time:
                # print("{} has entered here at {}".format(threadname, datetime.now().time()))
                try:
                    data = sock.recv(1024).decode("utf-8")
                except socket.error:
                    continue
                if (count%100)==0:
                    cur_time=time.time()
                if (count%100)==99:
                    rate=99/(time.time()-cur_time)
                fp.write(str(data)+','+ str(time.time())+','+ str(rate)+'\n')
                # fp.write(str(count)+','+ str(datetime.now().time())+','+ str(rate)+'\n')
                count+=1
                # try:
                #     count+=1
                # except KeyboardInterrupt:
                #     print("{} has entered here at {}".format(threadname, datetime.now().time()))
                #     exit_event.set()
                d= str(data).split(',')
                if count == 1:
                    print(count)
                    initial = int(d[-2]) - count - 1
                # print(initial, int(d[-2]))
                print(d[-5:-1], " Received:", count-1, " Data rate:",rate," Drop:",int(d[-2])-count-1-initial, " Port:", port)
                print("count:", count, "Rate:", rate)
                # if KeyboardInterrupt:
                #     print("{} has entered here at {}".format(threadname, datetime.now().time()))
                #     exit_event.set()
                if exit_event.is_set():
                    break
        except Exception as e: 
            print(e)
        finally:
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))
            sock.close()
    lock.release()
        
lock = threading.Lock()
thread1 = camThread(port1, filename1)
thread2 = camThread(port2, filename2)
thread3 = camThread(port3, filename3)
thread4 = camThread(port4, filename4)
thread5 = camThread(port5, filename5)
thread6 = camThread(port6, filename6)
thread7 = camThread(port7, filename7)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
print("Time up!!!!!!!!!!!!!!!!!!!!!")
