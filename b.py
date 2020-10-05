# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import socket
import time

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import gc
import sys

import cv2
from cv_bridge import CvBridge

import threading

'''
def callback_battery(data):
    video.x = 0
    #xx = str('%')
    #global x
    video.x = ("%s" %data.data)

def listener_battery():
    rospy.Subscriber("battery", String, callback_battery)
'''

class video(QMainWindow):
    def __init__(self):
    #def __init__(self, cam): 有用cam的時候
        super(video,self).__init__()
        #self.battery_str = self.x
        self.xx = str('%')
        self.a =1

        self.resize(1600, 1024)
        self.setWindowTitle('gui')    

        self.vF = QLabel()
        self.setCentralWidget(self.vF)
        self.vF.setGeometry(QtCore.QRect(160, 152, 960, 720)) 
        #位置x y  長 寬  位置是看左上角的點

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(1410, 890, 191, 131))
        #self.label_2.setText("")
        #圖片寫法好像不同？
        pix = QPixmap('aa.png')
        self.label_2.setPixmap(pix)
        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)
       
        # 设置视频显示在窗口中间,否则可以注释掉
        self.vF.setAlignment(Qt.AlignCenter)
        self.pushButton_camera = QPushButton(self)
        self.pushButton_camera.setGeometry(QtCore.QRect(30, 40, 200, 70))
        self.pushButton_camera.setObjectName("pushButton_camera")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_camera.setFont(font)
        self.pushButton_camera.setText("使用手動控制")
        #"開啟相機"

        self.battery_textBrowser1 = QTextBrowser(self)
        self.battery_textBrowser1.setGeometry(QtCore.QRect(830, 20, 220, 40))
        self.battery_textBrowser1.setObjectName("battery_textBrowser1")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.battery_textBrowser1.setFont(font)
        self.battery_textBrowser1.setText('大無人機電量： 0%s' %self.xx)
        self.battery_textBrowser1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.battery_textBrowser1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.battery_textBrowser = QTextBrowser(self)
        self.battery_textBrowser.setGeometry(QtCore.QRect(480, 20, 220, 40))
        self.battery_textBrowser.setObjectName("battery_textBrowser")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.battery_textBrowser.setFont(font)
        self.battery_textBrowser.setText('小無人機電量： 0%s' %self.xx)
        self.battery_textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.battery_textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.battery_textBrowser2 = QTextBrowser(self)
        self.battery_textBrowser2.setGeometry(QtCore.QRect(480, 90, 220, 40))
        self.battery_textBrowser2.setObjectName("battery_textBrowser2")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.battery_textBrowser2.setFont(font)
        self.battery_textBrowser2.setText('小無人機座標：(0,0)' )
        self.battery_textBrowser2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.battery_textBrowser2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.battery_textBrowser3 = QTextBrowser(self)
        self.battery_textBrowser3.setGeometry(QtCore.QRect(830, 90, 220, 40))
        self.battery_textBrowser3.setObjectName("battery_textBrowser3r")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.battery_textBrowser3.setFont(font)
        self.battery_textBrowser3.setText('大無人機座標：(0,0)' )
        self.battery_textBrowser3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.battery_textBrowser3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        #介入
        self.takeoff = QPushButton(self)
        self.takeoff.setGeometry(QtCore.QRect(30, 120, 200, 70))
        self.takeoff.setObjectName("pushButton_takeoff")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.takeoff.setFont(font)
        self.takeoff.setText("起飛")
        self.takeoff.clicked.connect(self.takeoff_click)
        
        self.land = QPushButton(self)
        self.land.setGeometry(QtCore.QRect(30, 200, 200, 70))
        self.land.setObjectName("pushButton_land")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.land.setFont(font)
        self.land.setText("降落")
        self.land.clicked.connect(self.land_click)

        self.movefront = QPushButton(self)
        self.movefront.setGeometry(QtCore.QRect(30, 280, 200, 70))
        self.movefront.setObjectName("pushButton_movefront")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.movefront.setFont(font)
        self.movefront.setText("向前")
        self.movefront.clicked.connect(self.movefront_click)
        
        self.moveback = QPushButton(self)
        self.moveback.setGeometry(QtCore.QRect(30, 360, 200, 70))
        self.moveback.setObjectName("pushButton_moveback")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.moveback.setFont(font)
        self.moveback.setText("向後")
        self.moveback.clicked.connect(self.moveback_click)

        self.moveleft = QPushButton(self)
        self.moveleft.setGeometry(QtCore.QRect(30, 440, 200, 70))
        self.moveleft.setObjectName("pushButton_moveleft")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.moveleft.setFont(font)
        self.moveleft.setText("向左")
        self.moveleft.clicked.connect(self.moveleft_click)

        self.moveright = QPushButton(self)
        self.moveright.setGeometry(QtCore.QRect(30, 520, 200, 70))
        self.moveright.setObjectName("pushButton_moveright")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.moveright.setFont(font)
        self.moveright.setText("向右")
        self.moveright.clicked.connect(self.moveright_click)

        #self.setfirst()
        #self.battery_renew()

        #self.w = QtCore.QThread()


        #刷新圖
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.load)
        self._timer.start(300)  
        #400

        #刷新電池電量
        self._timer_battery = QTimer(self)
        self._timer_battery.timeout.connect(self.battery_renew)
        self._timer_battery.join(1000)


    def load(self):
        rospy.Subscriber("image", Image, self.callback)
        #self.battery_renew()
        #rospy.Subscriber("battery", String, self.callback_battery)


    def callback(self, imgmsg):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
        img = cv2.resize(img, (960, 720))
        #self.w.wait()
        self.vF.setPixmap(QPixmap.fromImage(
            QImage(cv2.cvtColor(img, cv2.COLOR_BGR2RGB ),
                960,
                720,
                13)))


    def battery_renew(self):
        rospy.Subscriber("battery", String, self.callback_battery)

    def callback_battery(self,data):
        o = str('%')
        v1 = ("%s" %data.data)
        self.battery_textBrowser.setText('小無人機電量： %s%s' %(v1,o))

    

    def takeoff_click(self):
        a = 0
        a = 'takeoff'
        pub_direct.publish(a)

    def land_click(self):
        b = 0
        b = 'land'
        pub_direct.publish(b)
        
    def movefront_click(self):
        c = 0
        c = 'forward 30'
        pub_direct.publish(c)

    def moveback_click(self):
        d = 0
        d = 'back 30'
        pub_direct.publish(d)

    def moveleft_click(self):
        e = 0
        e = 'left 30'
        pub_direct.publish(e)

    def moveright_click(self):
        f = 0
        f = 'right 30'
        pub_direct.publish(f)


if __name__ == '__main__':
   
    ##pub_direct = rospy.Publisher('direct', String, queue_size=1)
    rospy.init_node('listener', anonymous=True)
    #pub = rospy.Publisher('image', Image, queue_size=1)
    #ao = '1'
    #pub_direct.publish(ao)

    app = QApplication(sys.argv)
    win = video()
    win.show()      
    sys.exit(app.exec_())