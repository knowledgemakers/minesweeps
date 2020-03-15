import serial, time, random
from random import randint


port = '/dev/ttyACM0'

####
####except sException:
####    port = '/dev/ttyACM1'
####
s1 = serial.Serial(port,9600)
s1.flushInput()

##while True:
##    if s1.inWaiting()>0:
##        inputValue = s1.read(1)
##        print(ord(inputValue))

def looper():
    port = '/dev/ttyACM0'
    s1 = serial.Serial(port,9600)
    s1.flushInput()
    for each in range(0,3):
        i=1
        s1.write(i.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.25)
        s1.write(b'3')
        #time.sleep(0.25)
        s1.write(b'4')
        #time.sleep(0.25)
        s1.write(b'5')
        #time.sleep(0.25)
        s1.write(b'4')
        #time.sleep(0.25)
        s1.write(b'3')
        #time.sleep(0.25)
    s1.flushInput()
    s1.close()
    s1.__del__()



def key_control():
    while True:
        n = input('Pin to activate:')
        
        n=int(n)
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        
def random_loop():
    n=50
    s1.write(n.to_bytes(1, byteorder='big', signed=True))
    while True:
        n = randint(2,9)
        n_up = n*2
        n_down=n_up+1
        s1.write(n_up.to_bytes(1, byteorder='big', signed=True))
        #print("Turning " + str(n) + " on")
        time.sleep(1)
        #print("Turning " + str(n) + " off")
        s1.write(n_down.to_bytes(1, byteorder='big', signed=True))

def line():
    n=50
    s1.write(n.to_bytes(1, byteorder='big', signed=True))
    counter=0
    while True:
        n=16
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=18
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        n=4
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=6
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=14
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=12
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=8
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=10
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        time.sleep(1)
        n=17
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=19
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        n=5
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=7
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=15
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=13
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=9
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        #time.sleep(0.5)
        n=11
        s1.write(n.to_bytes(1, byteorder='big', signed=True))
        time.sleep(0.5)
        counter+=1
        print(counter)



live = [5,6]

def random_control():
    
    while True:
        #n = input('Pin to activate:')
        t = random.randint(1,8)
        #t = live[n]
        t = int(t)
        print(t)
        if t == 1:
            s1.write(b'2')
        elif t == 2:
            s1.write(b'3')
        elif t == 3:
            s1.write(b'4')
        elif t == 4:
            s1.write(b'5')
        elif t == 5:
            s1.write(b'6')
        elif t == 6:
            s1.write(b'7')
        elif t == 7:
            s1.write(b'8')
        elif t == 8:
            s1.write(b'9')
##        elif n == 9:
##            s1.write(b'10')
##        elif n == 10:
##            s1.write(b'11')
##        elif n == 11:
##            s1.write(b'12')
##        elif n == 12:
##            s1.write(b'13')
        #elif n == 13:
        #    s1.write(b'14')
        else:
            pass

#random_control()
#looper()
try:
    key_control()
    #random_loop()
    #line()
finally:
    s1.flushInput()
    s1.close()
