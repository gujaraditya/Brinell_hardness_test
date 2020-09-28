
import sys
import numpy as np
import imutils
import time
import cv2
import math
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt5.uic import loadUi

start_detect=None
class lineeditfunc(QLineEdit):
    clicked=pyqtSignal()
    def __init__(self,widget):
        super(lineeditfunc,self).__init__(widget)
    def mousePressEvent(self,QMouseEvent):
        self.clicked.emit()
class Brinell(QDialog):


    def __init__(self):
        super(Brinell,self).__init__()
        loadUi('BrinellMainWindow.ui',self)
##        self.cap=cv2.VideoCapture(1)
        
        self.numbertext="2"
        self.capture=cv2.VideoCapture(0)
        self.start_spotdetect()
        self.MainText1=lineeditfunc(self)
        self.MainText2=lineeditfunc(self)
        self.MainText1.setFixedWidth(85)
        self.MainText1.move(135,145)
        self.MainText2.setFixedWidth(85)
        self.MainText2.move(358,145)
        self.MainText1.clicked.connect(self.numpadwindow1)
        self.MainText2.clicked.connect(self.numpadwindow2)
        self.minvalVar=self.MainText1.text()
        self.maxvalVar=self.MainText2.text()
        self.ExecuteButton.clicked.connect(self.ExecuteCommand)
        self.CloseButton.clicked.connect(self.close_allwindow)
##        self.start_detect.DisplayCombo.setText(combovalue)
##        c1=Numpad1()
##        c2=c1.okay1()
        
##        number_exp=" "
        

##        self.equation=StringVar()
##        self.equation.set('enter your expression')
    def numpadwindow1(self):
        self.firstNumpad=Numpad1()
        self.firstNumpad.show()
        
        
    def numpadwindow2(self):
        self.secondNumpad=Numpad2()
        self.secondNumpad.show()    

    def start_spotdetect(self):
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 290)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 210)
        self.timer=QTimer(self)
        
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)
        
    def update_frame(self):
        
        ret,self.image=self.capture.read()
##        self.image=cv2.flip(self.image,1)
        
        self.displayImage(self.image)
        
##        self.StartButton.clicked.connect(self.start_webcam)

    def displayImage(self,img):
        
##        self.spotdetect=loadUi('SpotDetection.ui')
        
        qformat=QImage.Format_Indexed8
        
        if len(img.shape)==3:
            if (img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage=outImage.rgbSwapped()
        

        
        
        self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
        self.imgLabel.setScaledContents(True)
            
            
            
    def ExecuteCommand(self):
        try:    
            self.img2=cv2.GaussianBlur(self.image,(3,3),0)
            self.img2=cv2.medianBlur(self.image,3)
            self.gray= cv2.cvtColor(self.img2,cv2.COLOR_BGR2GRAY)
            self.combo1value=str(mainwindow.comboBox1.currentText())
            self.combo2value=str(mainwindow.comboBox2.currentText())
            
      
            
            self.thresh=cv2.threshold(self.gray,100,255,cv2.THRESH_BINARY_INV)[1]
            
            self.kernel=np.ones((1,1),np.uint8)

            self.thresh=cv2.erode(self.thresh,self.kernel,iterations=2)
            self.thresh=cv2.dilate(self.thresh,self.kernel,iterations=2)
##            cv2.imshow("thresh",self.thresh)
            self.circles=cv2.HoughCircles(self.gray,cv2.HOUGH_GRADIENT,20,90)
            
            if self.circles is not None:

                self.img2, self.contours,self.hierarchy=cv2.findContours(self.thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if imutils.is_cv2():
                    self.contours=self.contours[0]
                else:
                    self.contours[1]
    ##            self.contours=self.contours[0]

                
                c=max(self.contours,key=cv2.contourArea)
                (x,y),radius =cv2.minEnclosingCircle(c)
                
                centre=(int(x),int(y))
                radius=int(radius)
                diameter=2*radius        
                d=diameter/40
                
                DIA=round(d,2)
                print (DIA)
                if DIA<5.2:
                    t=cv2.circle(self.image,centre,radius,(0,255,0),2)
    ##                cv2.circle(self.image,centre,6,(255,0,0),-1)
                    
                    b=2
                    h=0.5
                    value1=(float(math.pi)*float(self.combo2value))/b
                    
                    value2=float(self.combo2value)**int(b)
                    value3=d**b   
                    fvalue4=float(self.combo2value)-round(((round((value2),2)-value3)**h),2)    
                    BHM=float(self.combo1value)/round((float(value1)*float(fvalue4)),2)
                    BHMVALUE=round(float(BHM),2)
                    print (BHMVALUE)           
                    cv2.circle(t,centre,6,(255,0,0),-1)
                    self.meandiagDist.setText(str(DIA))
                    self.BHNLabel.setText(str(BHMVALUE))
                    self.minvalVar=mainwindow.MainText1.text()
                    self.maxvalVar=mainwindow.MainText2.text()
                    print ("min=",self.minvalVar)
                    print ("min=",self.maxvalVar)
                    if ((int(BHMVALUE)<=int(self.minvalVar)) or (int(BHMVALUE)>=int(self.maxvalVar))):
                        self.resultLabel.setText("Fail")
                        self.resultLabel.setStyleSheet('color: red')
                    elif ((int(BHMVALUE)>int(self.minvalVar)) and (int(BHMVALUE)<int(self.maxvalVar))):
                        self.resultLabel.setText("Pass")
                        self.resultLabel.setStyleSheet('color: green')
        except:
            if((self.combo1value=="Select")or(self.combo2value=="Select")):               
                self.Alertbox2=Alertdia()
                self.Alertbox2.show()
            else:   
                self.Alertbox1=Alert_minmax()
                self.Alertbox1.show()
        
##    def showtex(self,number_exp):
##        self.MainText1.clear()
##        self.MainText1.setText(str(number_exp))
##        print (str(number_exp))
##        self.MainText2.setText(number_exp)    
    
    def close_allwindow(self):
        sys.exit(0)        
class Alertdia(QDialog):
    def __init__(self):
        super(Alertdia,self).__init__()
        loadUi('AlertdiaBox.ui',self)
        self.OkButton.clicked.connect(self.okay)
    def okay(self):
        self.close()
class Alert_minmax(QDialog):
    def __init__(self):
        super(Alert_minmax,self).__init__()
        loadUi('Alert_minmax.ui',self)
        self.OkButton.clicked.connect(self.okay)


    def okay(self):
        self.close()
class Numpad1(QDialog):    
    
    def __init__(self):
        super(Numpad1,self).__init__()
        loadUi('BNumpad1.ui',self)
    
        
        
##        self.number_exp=StringVar()
        
##        self.numpad1=loadUi('Numpad1.ui')
##        self.numpad1.show()
        
##        self.equation=StringVar()
##        self.equation.set('enter your expression')
##        layout=QHBoxLayout()
##        lineEdit=QLineEdit()
##        
##        self.lineEdit.setText("enter your expression")
##        layout.addWidget(lineEdit)
        self.No1.clicked.connect(lambda:self.press(1))
        self.No2.clicked.connect(lambda:self.press(2))
        self.No3.clicked.connect(lambda:self.press(3))
        self.No4.clicked.connect(lambda:self.press(4))
        self.No5.clicked.connect(lambda:self.press(5))
        self.No6.clicked.connect(lambda:self.press(6))
        self.No7.clicked.connect(lambda:self.press(7))
        self.No8.clicked.connect(lambda:self.press(8))
        self.No9.clicked.connect(lambda:self.press(9))
        self.No0.clicked.connect(lambda:self.press(0))
        self.OkayButton.clicked.connect(self.okay1)
        self.ClrButton.clicked.connect(self.clear)
##        self.winnum1=Vickers()

    def press(self,num):
##        self.number_exp=StringVar()
##        print (num)       
        self.numbertext=str(num)
##        self.equation.set(self.number_exp)
        self.lineEdit.setText(self.lineEdit.text()+self.numbertext)
    def clear(self):
        
        self.lineEdit.setText(" ")
    def okay1(self):
        
        number_exp1=self.lineEdit.text()
        mainwindow.MainText1.setText(number_exp1)
        self.clear()
        self.close()
         
        
##        destroy()
class Numpad2(QDialog):
        
    def __init__(self):
        super(Numpad2,self).__init__()
        loadUi('BNumpad2.ui',self)
        
##        self.numpad2=loadUi('Numpad2.ui')
        
##        self.equation=StringVar()
##        self.equation.set('enter your expression')
##        self.lineEdit.setText(self.equation)
        self.No1.clicked.connect(lambda:self.press(1))
        self.No2.clicked.connect(lambda:self.press(2))
        self.No3.clicked.connect(lambda:self.press(3))
        self.No4.clicked.connect(lambda:self.press(4))
        self.No5.clicked.connect(lambda:self.press(5))
        self.No6.clicked.connect(lambda:self.press(6))
        self.No7.clicked.connect(lambda:self.press(7))
        self.No8.clicked.connect(lambda:self.press(8))
        self.No9.clicked.connect(lambda:self.press(9))
        self.No0.clicked.connect(lambda:self.press(0))
        self.OkayButton.clicked.connect(self.okay2)
        self.ClrButton.clicked.connect(self.clear)

    def press(self,num):
        self.numbertext=str(num)

        self.lineEdit.setText(self.lineEdit.text()+self.numbertext)    
    
        
    def clear(self):
        self.lineEdit.setText(" ")        

    def okay2(self):
        number_exp2=self.lineEdit.text()
##        self.MainText2.setText(self.lineEdit.text())
        mainwindow.MainText2.setText(number_exp2)
        self.close()        
        self.clear()
##        self.secondNumpad.destroy()
        

##    def okay2(self):
##        
##
##        self.max_value=self.number_exp
##        self.lineEdit2.set(self.number_exp)
##        
##        self.clear()
##        self.numpad2.destroy()

        
##class BrinellSpotdetection(QDialog):
##    def __init__(self):
##        super(BrinellSpotdetection,self).__init__()
##        loadUi('BrinellSpotDetection.ui',self)
##        self.combo1value=str(mainwindow.comboBox1.currentText())        
##        self.combo2value=str(mainwindow.comboBox2.currentText())
##        combovalue=str(self.combo1value+"/"+self.combo2value)
##        self.DisplayCombo.setText(str(combovalue))
##        self.ExecuteButton.clicked.connect(self.ExecuteCommand)
##        self.BackButton.clicked.connect(self.back)
##        self.CameraOn.clicked.connect(self.start_webcam)
##        
##    def start_webcam(self):
##        
##        
##    def back(self):
##        self.close()
        


               
                   
mainwindow=None
if __name__=='__main__':
    app=QApplication(sys.argv)
    mainwindow=Brinell()
    mainwindow.setWindowTitle('Brinell Hardness Test')



    #window.setGeometry(100,100,400,200)
    mainwindow.show()
    sys.exit(app.exec_())
