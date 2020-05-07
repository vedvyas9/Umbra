import time
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import serial as S1
import math
import pigpio

acceServoy=26
acceServox=17
acceServoz=23

boo=0


ser = S1.Serial('/dev/ttyACM0', 9600)


def choose():
    if(fin_bent()==1):
        SetAngle2(y1*100,acceServoz,piz)
    else:
        SetAngle3(y1*100,acceServoy,piy)
        SetAngle2(x1*100,acceServox,pix)
        


def fin_bent():
    line = ser.readline()
    for s in line.split():
        #if s.isdigit():
            f=int(s)
            if(f>(-600)):
                return 1
            else:
                return 0



def SetAngle2(angle,servoPin,pii):
    boo=0
    if(angle>157.0) :
       boo=150
    elif(boo<(-157.0)):
        boo=-150
    else:
        boo=translate(angle,-157,157,500,2500)
    
    pii.get_mode(servoPin)
    pii.set_servo_pulsewidth(servoPin, boo)
    pii.get_servo_pulsewidth(servoPin)
    return
def SetAngle3(angle,servoPin,pii):
    boo=0
    if(angle>157.0) :
       boo=150
    elif(boo<(-157.0)):
        boo=-150
    else:
        boo=translate(angle,-180,180,1500,500)
    
    pii.get_mode(servoPin)
    pii.set_servo_pulsewidth(servoPin, boo)
    pii.get_servo_pulsewidth(servoPin)
    return
def calc_xy(x,y,z):
    x2=x*x
    y2=y*y
    z2=z*z
    
    #res3 = math.sqrt(x2+y2)
    #res3=res3/z
    #accel_z=math.atan(res3)
    
    try:
        res=math.sqrt(y2+z2)
        res=x/res
        accel_x=math.atan(res)
    
        res1=math.sqrt(x2+z2)
        res1=y/res1
        accel_y=math.atan(res1)
    except:
        print('lol')
    finally:
        return accel_x,accel_y#,accel_z
    
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

piy = pigpio.pi()
piy.set_mode(acceServoy, pigpio.OUTPUT)

pix = pigpio.pi()
pix.set_mode(acceServox, pigpio.OUTPUT)

piz = pigpio.pi()
piz.set_mode(acceServoz, pigpio.OUTPUT)

accel = Adafruit_ADXL345.ADXL345()

while True:
    x, y, z = accel.read()
    print('X={0}, Y={1}, Z={2}, '.format(x, y, z))
    x1,y1=calc_xy(x,y,z)
    print(x1*100)
    #print(y1*100)
    #print(z1*100)
    #xx=translate(x,-220,190,0,180)
    #zz=translate(y,-35,0,0,180)
    #yy=translate(y,-240,230,0,180)
    #print(yy)
    #zz=translate(z,-40,45,0,180)
    #print('Y={0}'.format(yy))
    #print('X={0}'.format(xx))
    #print('Z={0}'.format(zz))
    #time.sleep(0.2)
    choose()
    #SetAngle3(x1*100,acceServox,pix)
    choose()
    #SetAngle2(y1*100,acceServoz,piz)
    #SetAngle2(x1*100,acceServox,pix)
    #time.sleep(0.06)
    #translate(z,-20,45,0,180)
    #piy.set_servo_pulsewidth(acceServoy,1000)
    #pix.set_servo_pulsewidth(acceServox,500)

