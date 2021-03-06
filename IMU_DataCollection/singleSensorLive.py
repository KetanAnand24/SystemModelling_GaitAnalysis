import matplotlib.pyplot as plt
import numpy as np
import socket
import time

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", 8888))
# s1.setblocking(0)

# s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s2.bind(("0.0.0.0", 7777))
# s2.setblocking(0)

axx = 0
ay = 1
az = 2
gx = 3
gy = 4
gz = 5
q1 = 6
q2 = 7
q3 = 8
q4 = 9
calcYaw = 10
calcPitch = 11
calcRoll = 12
Yaw = 13
Pitch = 14
Roll = 15
count = 16
timer = 17
hs = 18
dist = 19
gravaccx = 20
gravaccy = 21
gravaccz = 22

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)
y3 = np.zeros(display_values)
y2 = np.zeros(display_values)
y1 = np.zeros(display_values)
# y4 = np.zeros(display_values)
# y5 = np.zeros(display_values)
# y6 = np.zeros(display_values)

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-360, 360])
line1, = ax.plot(x, y1, label='yaw b')
line2, = ax.plot(x, y2, label='pitch b')
line3, = ax.plot(x, y3, label='roll b')
# line4, = ax.plot(x, y4, label='yaw c')
# line5, = ax.plot(x, y5, label='pitch c')
# line6, = ax.plot(x, y6, label='roll c')
ax.legend()

#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 15

k = 0
count = 0
rate = 0
while True:
    data1 = s1.recv(1024).decode("utf-8")
    if count == 0:
        initialtime = time.time()
    count+=1
    if time.time() - initialtime > 1:
        rate = count / (time.time() - initialtime)
        count = 0
    print(rate)
    d = str(data1).split(',')
    # data2 = s2.recv(1024).decode("utf-8")
    # d2 = str(data2).split(',')
    # print(d[-3])
    y1 = np.roll(y1, -1)
    y1[-1] = d[calcYaw]
    y2 = np.roll(y2, -1)
    y2[-1] = d[calcPitch]
    y3 = np.roll(y3, -1)
    y3[-1] = d[calcRoll]
    # y4 = np.roll(y4, -1)
    # y4[-1] = d2[calcYaw]
    # y5 = np.roll(y5, -1)
    # y5[-1] = d2[calcPitch]
    # y6 = np.roll(y6, -1)
    # y6[-1] = float(d2[az]) * 10
    # print(k)
    k = k + 1
    if k == r:
        line1.set_ydata(y1)
        line2.set_ydata(y2)
        line3.set_ydata(y3)
        # line4.set_ydata(y4)
        # line5.set_ydata(y5)
        # line6.set_ydata(y6)
        fig.canvas.draw()
        fig.canvas.flush_events()
        k = 0