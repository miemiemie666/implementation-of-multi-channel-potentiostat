######################################################
 # Editor : Zechuan Chen
 # Version: 3.0
 # Product: User Interface
 # Date:21.02.2023
######################################################
# coding=utf-8
from ui import Ui_MainWindow

import serial   #安装pyserial，但import serial，且不能安装serial
import serial.tools.list_ports #串口检测库
import sys,time
import pyqtgraph as pg
import math

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class MyMainWindow(QMainWindow):
    sersinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        # 串口无效
        self.ser = None
        self.send_num = 0
        self.receive_num = 0
        self.receive_str = ''
        # 记录最后发送的回车字符的变量
        self.rcv_enter = ''
        
        ############变量区###########
        self.yPointNum=0 #y轴点数
        self.floatData=0 #ion电压缓存
        self.S1=[]       
        self.S2=[]      #blank
        self.S3=[]      #mg1                      
        self.S4=[]      #ca1
        self.S5=[]      #k1
        self.S6=[]      #k2
        self.S7=[]      #ca2
        self.S8=[]      #mg2
        self.R1=[]; self.R2=[]; self.R3=[];self.R4=[]; self.R5=[]; self.R6=[];self.R7=[]; self.R8=[]; 
        self.I1=[]; self.I2=[]; self.I3=[];self.I4=[]; self.I5=[]; self.I6=[];self.I7=[]; self.I8=[]; 
        self.Z1=[]; self.Z2=[]; self.Z3=[];self.Z4=[]; self.Z5=[]; self.Z6=[];self.Z7=[]; self.Z8=[];
        self.F1=[]; self.F2=[]; self.F3=[];self.F4=[]; self.F5=[]; self.F6=[];self.F7=[]; self.F8=[];

        #k1曲线拟合参数k和b,以及R^2
        self.k1_funtion_kb=(0,0,0)  #k
        self.k2_funtion_kb=(0,0,0)
        self.k1_concentration=0
        self.k2_concentration=0
        self.ca1_funtion_kb=(0,0,0) #ca
        self.ca2_funtion_kb=(0,0,0)
        self.ca1_concentration=0
        self.ca2_concentration=0
        self.c_mg1=0                 #mg
        self.c_mg2=0
        self.k_mg1=0
        self.k_mg2=0
        self.k_mgk1=0
        self.k_mgk2=0
        self.k_mgca1=0
        self.k_mgca2=0

        #Voltammetry
        self.E_begin=0
        self.E_end=0
        self.E_step=0
        self.E_scanrate=0
        self.E_numofscan=0
        self.E_pulse=0
        self.E_Tpulse=0
        self.E_amplitude=0
        self.E_frequency=0
        
        #EIS
        self.Z_unknown=0;

        self.R_refNum = 2;
        self.R_unkNum = 8;

        self.P_startFREQ = 80000;
        self.P_freqINCR = 1000;
        self.P_numINCR = 40;
        self.P_refRESIST = 10000;
        ###############################

        # 实例化一个定时器
        self.timer = QTimer(self)
        self.timer_send = QTimer(self)

        # 定时器调用读取串口接收数据
        self.timer.timeout.connect(self.recv)
        # 定时发送
        self.timer_send.timeout.connect(self.send)

        # 刷新一下串口的列表
        self.refresh()
        #设置背景色
        self.__ui.graphicsView.setBackground('w')

        # 菜单栏Version/Support
        self.__ui.actionVersion.triggered.connect(self.version)
        self.__ui.actionSupport.triggered.connect(self.support)
        # 刷新串口外设按钮
        self.__ui.pushButton.clicked.connect(self.refresh)
        # 打开关闭串口按钮
        self.__ui.pushButton_2.clicked.connect(self.open_close)
        # 发送数据按钮
        self.__ui.pushButton_3.clicked.connect(self.send)
        # 清除窗口
        self.__ui.pushButton_4.clicked.connect(self.clear)
        # 保存数据
        self.__ui.pushButton_5.clicked.connect(self.txt_save)
        self.__ui.pushButton_6.clicked.connect(self.txt_saveMore)
        self.__ui.actionSave_as_CSV.triggered.connect(self.txttocsv_save)
        # 定时发送
        self.__ui.checkBox_3.clicked.connect(self.send_timer_box)
        #连接信号与槽
        self.sersinOut.connect(self.graphDraw)
        #切换模式
        #self.__ui.comboBox_6.activated.connect(self.XXxX) #添加槽函数,如清屏幕，换Tab页等
        self.__ui.comboBox_6.currentIndexChanged.connect(self.mode_change)#添加槽函数,如清屏幕，换Tab页等
        self.__ui.tabWidget.currentChanged.connect(self.mode_change2)#换Tab页等
        ######画图##############
        #tab_1的控件 K1,k2,Ca1,Ca2,Mg1,Mg2
        self.__ui.pushButton_7.clicked.connect(self.K1_detection)
        self.__ui.pushButton_8.clicked.connect(self.K2_detection)
        self.__ui.pushButton_9.clicked.connect(self.Ca1_detection)
        self.__ui.pushButton_10.clicked.connect(self.Ca2_detection)
        self.__ui.pushButton_11.clicked.connect(self.Mg1_detection)
        self.__ui.pushButton_12.clicked.connect(self.Mg2_detection)
        self.__ui.pushButton_13.clicked.connect(self.Blank_detection)
        self.__ui.lineEdit_2.returnPressed.connect(self.curve_set)
        self.__ui.lineEdit_3.returnPressed.connect(self.constant_set)
        #tab_2的控件
        self.__ui.lineEdit_4.returnPressed.connect(self.parameter_E_begin)
        self.__ui.lineEdit_5.returnPressed.connect(self.parameter_E_end)
        self.__ui.lineEdit_6.returnPressed.connect(self.parameter_E_step)
        self.__ui.lineEdit_7.returnPressed.connect(self.parameter_E_scanrate)
        self.__ui.lineEdit_8.returnPressed.connect(self.parameter_E_numofscan)
        self.__ui.comboBox_9.currentIndexChanged.connect(self.set_current)
        self.__ui.pushButton_14.clicked.connect(self.start_CV_LSV)
        #tab_3的控件
        self.__ui.lineEdit_22.returnPressed.connect(self.parameter_E_pulse)
        self.__ui.lineEdit_21.returnPressed.connect(self.parameter_E_Tpulse)
        self.__ui.lineEdit_19.returnPressed.connect(self.parameter_E_begin)
        self.__ui.lineEdit_18.returnPressed.connect(self.parameter_E_end)
        self.__ui.lineEdit_17.returnPressed.connect(self.parameter_E_step)
        self.__ui.lineEdit_16.returnPressed.connect(self.parameter_E_scanrate)
        self.__ui.lineEdit_20.returnPressed.connect(self.parameter_E_numofscan)
        self.__ui.comboBox_13.currentIndexChanged.connect(self.set_current)
        self.__ui.pushButton_23.clicked.connect(self.start_Other)
        #tab_4的控件
        self.__ui.lineEdit_24.returnPressed.connect(self.parameter_E_amplitude)
        self.__ui.lineEdit_28.returnPressed.connect(self.parameter_E_frequency)
        self.__ui.lineEdit_27.returnPressed.connect(self.parameter_E_begin)
        self.__ui.lineEdit_25.returnPressed.connect(self.parameter_E_end)
        self.__ui.lineEdit_23.returnPressed.connect(self.parameter_E_step)
        self.__ui.lineEdit_26.returnPressed.connect(self.parameter_E_numofscan)
        self.__ui.comboBox_14.currentIndexChanged.connect(self.set_current)
        self.__ui.pushButton_24.clicked.connect(self.start_Other)
        #tab_5的控件NPV
        self.__ui.lineEdit_32.returnPressed.connect(self.parameter_E_Tpulse)
        self.__ui.lineEdit_33.returnPressed.connect(self.parameter_E_scanrate)
        self.__ui.lineEdit_34.returnPressed.connect(self.parameter_E_begin)
        self.__ui.lineEdit_31.returnPressed.connect(self.parameter_E_end)
        self.__ui.lineEdit_29.returnPressed.connect(self.parameter_E_step)
        self.__ui.lineEdit_30.returnPressed.connect(self.parameter_E_numofscan)
        self.__ui.comboBox_15.currentIndexChanged.connect(self.set_current)
        self.__ui.pushButton_25.clicked.connect(self.start_Other)
        #tab_6的控件
        self.__ui.lineEdit_36.returnPressed.connect(self.parameter_P_startFREQ)
        self.__ui.lineEdit_35.returnPressed.connect(self.parameter_P_freqINCR)
        self.__ui.lineEdit_37.returnPressed.connect(self.parameter_P_numINCR)
        self.__ui.lineEdit_38.returnPressed.connect(self.parameter_P_refRESIST)
        self.__ui.lineEdit_39.returnPressed.connect(self.parameter_R_refNum)
        self.__ui.lineEdit_40.returnPressed.connect(self.parameter_R_unkNum)
        self.__ui.comboBox_16.currentIndexChanged.connect(self.eis_mode)
        self.__ui.pushButton_26.clicked.connect(self.start_EIS)
        self.__ui.comboBox_10.currentIndexChanged.connect(self.set_EIS_graph)
        

    
    #############################画图######################################


    def test(self):
        pass



    def graphDraw(self):
       
        if self.__ui.comboBox_6.currentText()=='Open Circuit Potentiometry':    
            yPointLimit = 1000 #y数据的最大个数
            
            if self.receive_str.startswith(b'S2='): #判断是否是S2开头的数据 blank 
                if self.yPointNum<yPointLimit:
                    self.yPointNum=self.yPointNum+1
                    self.floatData=float(self.receive_str[3:9])
                    self.S2.append(self.floatData)
                    #print(S2[len(S2)-1])
                if self.yPointNum>=yPointLimit:  #到上限以后，删1数据加1数据 
                    self.yPointNum=self.yPointNum+1
                    self.floatData=float(self.receive_str[3:9])
                    self.S2.append(self.floatData)
                    #print(S2[len(S2)-1])
                    self.S2=self.S2[1:] 

            elif self.receive_str.startswith(b'S3='): #判断是否是S3开头的数据  mg1
                if self.yPointNum<yPointLimit:                
                    self.floatData=float(self.receive_str[3:9])
                    self.S3.append(self.floatData)
                    #print(S3[len(S3)-1])
                if self.yPointNum>=yPointLimit:  #到上限以后，删1数据加1数据
                    self.floatData=float(self.receive_str[3:9])
                    self.S3.append(self.floatData)
                    #print(S3[len(S3)-1])
                    self.S3=self.S3[1:] 
                #计算mg2浓度  
                if (self.k1_funtion_kb[0]!=0)&(self.ca1_funtion_kb[0]!=0)&(self.k_mgca1!=0):  #判断是否有拟合完成,随意判断，可用c_mg2,k_mg2等               
                    self.mg1_concentration=math.log(10**((self.floatData-self.c_mg1)/self.k_mg1)-self.k_mgk1*((self.k1_concentration+self.k2_concentration)/2)**2-self.k_mgca1*((self.ca1_concentration+self.ca2_concentration)/2),10)
                    self.mg1_concentration=round(self.mg1_concentration,3)    #保留3位小数
                    dis_concentration = 'Mg1: 10^'+str(self.mg1_concentration)+'mol/L'
                    self.__ui.label_11.setText(dis_concentration)  

            elif self.receive_str.startswith(b'S4='): #判断是否是S4开头的数据  ca1
                if self.yPointNum<yPointLimit:
                    self.floatData=float(self.receive_str[3:9])
                    self.S4.append(self.floatData)
                    #print(S4[len(S4)-1])
                if self.yPointNum>=yPointLimit:  #到上限以后，删1数据加1数据
                    self.floatData=float(self.receive_str[3:9])
                    self.S4.append(self.floatData)
                    #print(S4[len(S4)-1])
                    self.S4=self.S4[1:] 
                #计算ca1浓度  
                if (self.ca1_funtion_kb[0]!=0):  #判断是否有拟合完成                 
                    self.ca1_concentration=-1*((self.floatData-self.ca1_funtion_kb[1])/self.ca1_funtion_kb[0])
                    self.ca1_concentration=round(self.ca1_concentration,3)    #保留3位小数
                    dis_concentration = 'ca1: 10^'+str(self.ca1_concentration)+'mol/L'
                    self.__ui.label_10.setText(dis_concentration)  


            elif self.receive_str.startswith(b'S5='): #判断是否是S5开头的数据  k1
                if self.yPointNum<yPointLimit:               
                    self.floatData=float(self.receive_str[3:9])
                    self.S5.append(self.floatData)
                    #print(S5[len(S5)-1])
                if self.yPointNum>=yPointLimit:  #到上限以后，删1数据加1数据
                    self.floatData=float(self.receive_str[3:9])
                    self.S5.append(self.floatData)
                    #print(S5[len(S5)-1])
                    self.S5=self.S5[1:] 
                #计算k1浓度  
                if (self.k1_funtion_kb[0]!=0):  #判断是否有拟合完成                 
                    #self.k1_concentration=-1*((0.444-self.k1_funtion_kb[1])/self.k1_funtion_kb[0]) #test
                    self.k1_concentration=-1*((self.floatData-self.k1_funtion_kb[1])/self.k1_funtion_kb[0])
                    self.k1_concentration=round(self.k1_concentration,3)    #保留3位小数
                    dis_concentration = 'K1: 10^'+str(self.k1_concentration)+'mol/L'
                    self.__ui.label_9.setText(dis_concentration)                                  


            elif self.receive_str.startswith(b'S6='): #判断是否是S6开头的数据  k2
                if self.yPointNum<yPointLimit:
                    self.floatData=float(self.receive_str[3:9])
                    self.S6.append(self.floatData)
                    #print(S6[len(S6)-1])
                if self.yPointNum>=yPointLimit:  
                    self.floatData=float(self.receive_str[3:9])
                    self.S6.append(self.floatData)
                    #print(S6[len(S6)-1])
                    self.S6=self.S6[1:] 
                #计算k2浓度  
                if (self.k2_funtion_kb[0]!=0):  #判断是否有拟合完成                 
                    self.k2_concentration=-1*((self.floatData-self.k2_funtion_kb[1])/self.k2_funtion_kb[0])
                    self.k2_concentration=round(self.k2_concentration,3)    #保留3位小数
                    dis_concentration = 'K2: 10^'+str(self.k2_concentration)+'mol/L'
                    self.__ui.label_12.setText(dis_concentration)    

            elif self.receive_str.startswith(b'S7='): #判断是否是S7开头的数据  ca2
                if self.yPointNum<yPointLimit:
                    self.floatData=float(self.receive_str[3:9])
                    self.S7.append(self.floatData)
                    #print(S7[len(S7)-1])
                if self.yPointNum>=yPointLimit:  #到上限以后，删1数据加1数据
                    #self.__ui.graphicsView.clear()
                    #self.yPointNum=self.yPointNum+1
                    self.floatData=float(self.receive_str[3:9])
                    self.S7.append(self.floatData)
                    #print(S7[len(S7)-1])
                    self.S7=self.S7[1:] 
                    #计算ca2浓度  
                if (self.ca2_funtion_kb[0]!=0):  #判断是否有拟合完成                 
                    self.ca2_concentration=-1*((self.floatData-self.ca2_funtion_kb[1])/self.ca2_funtion_kb[0])
                    self.ca2_concentration=round(self.ca2_concentration,3)    #保留3位小数
                    dis_concentration = 'ca2: 10^'+str(self.ca2_concentration)+'mol/L'
                    self.__ui.label_13.setText(dis_concentration)  

            elif self.receive_str.startswith(b'S8='): #判断是否是S8开头的数据  mg2
                if self.yPointNum<yPointLimit:
                    self.floatData=float(self.receive_str[3:9])
                    self.S8.append(self.floatData)
                    #print(S8[len(S8)-1])
                if self.yPointNum>=yPointLimit: 
                    self.floatData=float(self.receive_str[3:9])
                    self.S8.append(self.floatData)
                    #print(S8[len(S8)-1])
                    self.S8=self.S8[1:] 
                #计算mg2浓度  
                if (self.k2_funtion_kb[0]!=0)&(self.ca2_funtion_kb[0]!=0)&(self.k_mgca2!=0):  #判断是否有拟合完成,随意判断，可用c_mg2,k_mg2等               
                    self.mg2_concentration=math.log(10**((self.floatData-self.c_mg2)/self.k_mg2)-self.k_mgk2*((self.k1_concentration+self.k2_concentration)/2)**2-self.k_mgca2*((self.ca1_concentration+self.ca2_concentration)/2),10)
                    self.mg2_concentration=round(self.mg2_concentration,3)    #保留3位小数
                    dis_concentration = 'Mg2: 10^'+str(self.mg2_concentration)+'mol/L'
                    self.__ui.label_14.setText(dis_concentration)                   


            self.__ui.graphicsView.clear()
            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Open Circuit potentiometry')           
            self.__ui.graphicsView.setLabel("left", "Voltage")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Time")
            #self.__ui.graphicsView.plot(self.S1,pen=pg.mkPen('b') ) 
            self.__ui.graphicsView.plot(self.S2,pen=pg.mkPen(color=(0,0,0),width=3))  #blank black
            self.__ui.graphicsView.plot(self.S3,pen=pg.mkPen('r',width=3))             #Mg red
            self.__ui.graphicsView.plot(self.S8,pen=pg.mkPen(color=(255,165,0),width=3)) 
            self.__ui.graphicsView.plot(self.S5,pen=pg.mkPen('y',width=3) )            #K yellow
            self.__ui.graphicsView.plot(self.S6,pen=pg.mkPen('g',width=3) ) 
            self.__ui.graphicsView.plot(self.S4,pen=pg.mkPen('b',width=3) )         ##Ca blue
            self.__ui.graphicsView.plot(self.S7,pen=pg.mkPen(color=(139,0,255),width=3) ) 

            self.__ui.graphicsView.setYRange(0,0.7)

            #self.__ui.graphicsView.enableAutoRange(axis='x', enable=False)  # 自动调整坐标轴范围
            # 到达yPointLimit后，左移图像
            #if self.yPointNum >= yPointLimit:
                #self.__ui.graphicsView.setXRange(self.yPointNum - yPointLimit, self.yPointNum)
                
                    
            
        elif self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':  
            
            if self.receive_str.startswith(b'ce='): #
                self.floatData=float(self.receive_str[3:9])
                self.S2.append(self.floatData) #2.4V
                #print(self.S2)
            if self.receive_str.startswith(b'we='): #
                self.floatData=float(self.receive_str[3:9])
                self.S3.append(self.floatData)
                #print(self.S3)

            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Cyclic Voltammetry')           
            self.__ui.graphicsView.setLabel("left", "Current")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Voltage")
            try:             
                if len(self.S2)==len(self.S3) and len(self.S2)>2:
                    if self.S2[len(self.S2)-1]>self.S2[len(self.S2)-2] :
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(125,120,120),width=3))
                    else:
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(0,0,0),width=3))
            except:
                pass
       
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':
            if self.receive_str.startswith(b'ce='): #
                self.floatData=float(self.receive_str[3:9])
                self.S2.append(self.floatData) #2.4V
                #print(self.S2)
            if self.receive_str.startswith(b'we='): #
                self.floatData=float(self.receive_str[3:9])
                self.S3.append(self.floatData)
                #print(self.S3)
            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Differential Pulse Voltammetry')           
            self.__ui.graphicsView.setLabel("left", "Current")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Voltage")
            try:             
                if len(self.S2)==len(self.S3) and len(self.S2)>2:
                    if self.S2[len(self.S2)-1]>self.S2[len(self.S2)-2] :
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(125,120,120),width=3))
                    else:
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(0,0,0),width=3))
            except:
                pass

        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':
            if self.receive_str.startswith(b'ce='): #
                self.floatData=float(self.receive_str[3:9])
                self.S2.append(self.floatData) #2.4V
                #print(self.S2)
            if self.receive_str.startswith(b'we='): #
                self.floatData=float(self.receive_str[3:9])
                self.S3.append(self.floatData)
                #print(self.S3)
            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Square Wave Voltammetry')           
            self.__ui.graphicsView.setLabel("left", "Current")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Voltage")
            try:             
                if len(self.S2)==len(self.S3) and len(self.S2)>2:
                    if self.S2[len(self.S2)-1]>self.S2[len(self.S2)-2] :
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(125,120,120),width=3))
                    else:
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(0,0,0),width=3))
            except:
                pass

        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':
            if self.receive_str.startswith(b'ce='): #
                self.floatData=float(self.receive_str[3:9])
                self.S2.append(self.floatData) #2.4V
                #print(self.S2)
            if self.receive_str.startswith(b'we='): #
                self.floatData=float(self.receive_str[3:9])
                self.S3.append(self.floatData)
                #print(self.S3)
            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Normal Pulse Voltammetry')           
            self.__ui.graphicsView.setLabel("left", "Current")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Voltage")
            try:             
                if len(self.S2)==len(self.S3) and len(self.S2)>2:
                    if self.S2[len(self.S2)-1]>self.S2[len(self.S2)-2] :
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(125,120,120),width=3))
                    else:
                        self.__ui.graphicsView.clear()
                        self.__ui.graphicsView.plot(self.S2,self.S3,pen=pg.mkPen(color=(0,0,0),width=3))
            except:
                pass
        
        elif self.__ui.comboBox_6.currentText()=='Electrochemical Impedance Spectroscopy':
            
            if self.receive_str.startswith(b'R1='): #方法1
                #self.floatData=float(self.receive_str[3:12]) #方法2,不行，原因带空格识别不了
                #self.R1.append(self.floatData) #2.4V
                #print(self.R1)
                variable, value = self.receive_str.decode().split("=")  # split the string into a list containing the data
                self.floatData = float(value )   # value tofloat          
                self.R1.append(self.floatData) 

            if self.receive_str.startswith(b'I1='): #方法1

                variable, value = self.receive_str.decode().split("=")  # split the string into a list containing the data
                self.floatData = float(value )   # value tofloat
                self.I1.append(self.floatData)




            self.__ui.graphicsView.setBackground('w')
            self.__ui.graphicsView.showGrid(x=True, y=True)#显示网格
            self.__ui.graphicsView.setTitle('Electrochemical Impedance Spectroscop')           
            self.__ui.graphicsView.setLabel("left", "Z_im")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Z_re")
            try: 
                if self.__ui.comboBox_10.currentText()=='Re(Z)-Im(Z)':                     
                    if len(self.R1)==len(self.I1) and len(self.R1)>2:
                        if self.R1[len(self.R1)-1]>self.R1[len(self.R1)-2] :
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.R1, self.I1, pen=None, symbol='o', symbolBrush=(0, 0, 0), symbolSize=8)
                    else:
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.R1, self.I1, pen=None, symbol='o', symbolBrush=(0, 0, 0), symbolSize=8)
                elif self.__ui.comboBox_10.currentIndex()==1:
                    self.__ui.graphicsView.setLabel("bottom", "f(Hz)")
                    if len(self.R1)==len(self.I1) and len(self.R1)>2:
                        if self.R1[len(self.R1)-1]>self.R1[len(self.R1)-2] :
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.R1,pen=pg.mkPen(color=(255,165,0),width=3))                             
                    else:
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.R1,self.I1,pen=pg.mkPen(color=(0,0,0),width=3))
                elif self.__ui.comboBox_10.currentIndex()==2:
                    self.__ui.graphicsView.setLabel("bottom", "f(Hz)")
                    if len(self.R1)==len(self.I1) and len(self.R1)>2:
                        #if self.R1[len(self.R1)-1]>self.R1[len(self.R1)-2] :
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.I1,pen=pg.mkPen(color=(255,0,255),width=3))                           
                    else:
                            self.__ui.graphicsView.clear()
                            self.__ui.graphicsView.plot(self.R1,self.I1,pen=pg.mkPen(color=(0,0,0),width=3))

            except:
                pass
        



    # 检测串口
    def refresh(self):
        port_list = list(serial.tools.list_ports.comports())  # 检测串口
        if len(port_list) <= 0:
            print("No used com!")
        else:
            self.__ui.comboBox.clear()
            for port in port_list:
                self.__ui.comboBox.addItem(port[0])

    # 打开关闭串口
    def open_close(self, btn_sta):
        if btn_sta == True:
            try:
                # 输入参数'COM13',115200
                comNum = self.__ui.comboBox.currentText()
                baudRate = int(self.__ui.comboBox_4.currentText())
                dataBit = int(self.__ui.comboBox_2.currentText())
                parityBit = self.__ui.comboBox_3.currentText()
                stopBit = int(self.__ui.comboBox_5.currentText())
                self.ser = serial.Serial(comNum, baudRate, dataBit, parityBit, stopBit, timeout=0.2)
            except:
                QMessageBox.critical(
                    self, 'pycom', 'No serial port available or the current serial port is occupied')  # 没有可用的串口或当前串口被占用
                self.__ui.pushButton_2.setChecked(False)
                self.__ui.pushButton_2.setText("Open")
                return None

            # 字符间隔超时时间设置
            self.ser.interCharTimeout = 0.001
            # 1ms的测试周期
            self.timer.start(2)
            self.__ui.pushButton_2.setChecked(True)
            self.__ui.pushButton_2.setText("Close")
            print('open')
        else:
            # 关闭定时器，停止读取接收数据
            self.timer_send.stop()
            self.timer.stop()

            try:
                # 关闭串口
                self.ser.close()
            except:
                QMessageBox.critical(
                    self, 'pycom', 'Failed to close serial port')  # 关闭串口失败
                return None

            self.ser = None
            self.__ui.pushButton_2.setText("Open")
            print('close!')

    # 串口发送数据处理
    def send(self):
        '''
        未解决BUG:
        1.输入框是带格式输入的
        2.换行只能按回车，输入\r \n无效 (猜测是输入转码了)
        '''
        if self.ser != None:
            input_s = self.__ui.textEdit.toPlainText()
            if input_s != "":

                # 发送字符
                if (self.__ui.checkBox.isChecked() == False):
                    input_s = input_s.encode('utf-8')  # 没事别用gbk
                else:
                    # 发送十六进制数据
                    input_s = input_s.strip()  # 删除前后的空格
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)

                        except ValueError:
                            print('input hex data!')
                            # 请输入十六进制数据，以空格分开!
                            QMessageBox.critical(self, 'pycom', 'input hex data!')
                            self.__ui.checkBox.setChecked(False)
                            return None

                        input_s = input_s[2:]
                        input_s = input_s.strip()

                        # 添加到发送列表中
                        send_list.append(num)
                    input_s = bytes(send_list)

                print('Send:', input_s)
                # 发送数据
                try:
                    num = self.ser.write(input_s)
                except:

                    self.timer_send.stop()
                    self.timer.stop()
                    # 串口拔出错误，关闭定时器
                    self.ser.close()
                    self.ser = None

                    # 设置为打开按钮状态
                    self.pushButton_2.setChecked(False)
                    self.pushButton_2.setText("Open")
                    print('serial error send!')
                    return None

                self.send_num = self.send_num + num
                dis = 'Send: ' + \
                    '{:d}'.format(self.send_num) + '  Receive: ' + \
                    '{:d}'.format(self.receive_num)
                self.__ui.label_6.setText(dis)
                # print('send!')
            else:
                print('none data input!')

        else:
            # 停止发送定时器
            self.timer_send.stop()
            QMessageBox.critical(
                self, 'error', 'Please open the serial port')  # 请打开串口

    def send_lindEdit(self, input_s):
        if self.ser != None:           
            if input_s != "":
                # 发送字符              
                input_s = input_s.encode('utf-8')  # 没事别用gbk

                print('Send:', input_s)
                # 发送数据
                try:
                    num = self.ser.write(input_s)
                except:

                    self.timer_send.stop()
                    self.timer.stop()
                    # 串口拔出错误，关闭定时器
                    self.ser.close()
                    self.ser = None
                  
                    print('serial error send!')
                    return None

                self.send_num = self.send_num + num
                dis = 'Send: ' + \
                    '{:d}'.format(self.send_num) + '  Receive: ' + \
                    '{:d}'.format(self.receive_num)
                self.__ui.label_6.setText(dis)
                # print('send!')
            else:
                print('none data input!')

        else:
            # 停止发送定时器
            QMessageBox.critical(
                self, 'error', 'Please open the serial port')  # 请打开串口

    # 定时发送数据
    def send_timer_box(self):

        if self.__ui.checkBox_3.isChecked():
            time = self.__ui.lineEdit.text()

            try:
                time_val = int(time, 10)
            except ValueError:
                QMessageBox.critical(
                    self, 'pycom', 'Please enter a valid timing!')
                self.__ui.checkBox_3.setChecked(False)
                return None

            if time_val == 0:
                QMessageBox.critical(
                    self, 'pycom', 'Please enter a valid timing!')
                self.__ui.checkBox_3.setChecked(False)
                return None
            # 定时间隔发送
            self.timer_send.start(time_val)
         
        else:
            self.timer_send.stop()

    # 串口接收数据处理
    def recv(self):    
        try:
            num = self.ser.inWaiting()
        except:

            self.timer_send.stop()
            self.timer.stop()

            # 串口拔出错误，关闭定时器
            self.ser.close()
            self.ser = None

            # 设置为打开按钮状态
            self.__ui.pushButton_2.setChecked(False)
            self.__ui.pushButton_2.setText("Open")
            print('serial error!')
            return None
        if(num > 0):
            # 有时间会出现少读到一个字符的情况，还得进行读取第二次，所以多读一个
            #data = self.ser.read(num)
            data = self.ser.readline(num)
            self.receive_str= data

            # 调试打印输出数据
            print('Receive:', self.receive_str)
            num = len(self.receive_str)            

            # 十六进制显示
            if self.__ui.checkBox_2.isChecked():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                out_s = data.decode('iso-8859-1')  # gbk，多字节速度快会崩溃，用iso-8859-1

                if self.rcv_enter == '\r':
                    # 上次有回车未显示，与本次一起显示
                    out_s = '\r' + out_s
                    self.rcv_enter = ''

                if out_s[-1] == '\r':
                    # 如果末尾有回车，留下与下次可能出现的换行一起显示，解决textEdit控件分开2次输入回车与换行出现2次换行的问题
                    out_s = out_s[0:-1]
                    self.rcv_enter = '\r'

            # 把字符串显示到窗口中去
            self.__ui.textBrowser.insertPlainText(out_s)
            #print(out_s)

            #发送信号
            self.sersinOut.emit(out_s)

            # 统计接收字符的数量
            self.receive_num = self.receive_num + num
            dis = 'Send: ' + \
                '{:d}'.format(self.send_num) + '  Receive: ' + \
                '{:d}'.format(self.receive_num)
            self.__ui.label_6.setText(dis)
            # 先把光标移到到最后
            cursor = self.__ui.textBrowser.textCursor()
            cursor.selectionEnd()
            self.__ui.textBrowser.setTextCursor(cursor)
        else:
            # 此时回车后面没有收到换行，就把回车发出去
            if self.rcv_enter == '\r':
                # 先把光标移到到最后
                cursor = self.__ui.textBrowser.textCursor()
                cursor.selectionEnd()
                self.__ui.textBrowser.setTextCursor(cursor)
                self.__ui.textBrowser.insertPlainText('\r')
                self.rcv_enter = ''

    # 清除窗口操作y
    def clear(self):
            self.__ui.textBrowser.clear()
            self.send_num = 0
            self.receive_num = 0
            dis = 'Send: ' + \
                '{:d}'.format(self.send_num) + '  Receive: ' + \
                '{:d}'.format(self.receive_num)
            self.__ui.label_6.setText(dis)

            #图像清除
            self.__ui.graphicsView.clear()#清除图像 
            self.S1=self.S1[0:0]
            self.S2=self.S2[0:0]
            self.S3=self.S3[0:0]
            self.S4=self.S4[0:0]
            self.S5=self.S5[0:0]
            self.S6=self.S6[0:0]   
            self.S7=self.S7[0:0]
            self.S8=self.S8[0:0]
            self.yPointNum=0
            #EIS
            self.R1=[]; self.R2=[]; self.R3=[];self.R4=[]; self.R5=[]; self.R6=[];self.R7=[]; self.R8=[]; 
            self.I1=[]; self.I2=[]; self.I3=[];self.I4=[]; self.I5=[]; self.I6=[];self.I7=[]; self.I8=[]; 
            self.Z1=[]; self.Z2=[]; self.Z3=[];self.Z4=[]; self.Z5=[]; self.Z6=[];self.Z7=[]; self.Z8=[];
            self.F1=[]; self.F2=[]; self.F3=[];self.F4=[]; self.F5=[]; self.F6=[];self.F7=[]; self.F8=[];

    # 保存数据
    def txt_save(self):

        try:
            txtFile = open('data.txt', 'w')
            strText = self.__ui.textBrowser.toPlainText()
            txtFile.write(strText)
            txtFile.close()

            data_dict = {}
            strText=strText.split('\n')
            strText = strText[:-1]
            for i in strText:
                if i[2]=='=':       
                    #print(i)
                    i=i.split('=')
                    #print(i)
                    if i[0] not in data_dict:
                        data_dict[i[0]] = []
                        data_dict[i[0]].append(i[1])
                    else:
                        data_dict[i[0]].append(i[1])
            data_dict=dict(sorted(data_dict.items())) #按照key排序

            with open('data.csv', 'w') as f:
                delimiter = ','
                for key, value in data_dict.items():
                    line = key + delimiter
                    for num in value:
                        line = line + str(num) + delimiter

                    f.write(line + '\n')       

            QMessageBox.information(self, 'Tips', 'Succeed to save!')
        except:
            print('Failed tu save!')
            QMessageBox.warning(self, 'Tips', 'Failed to save!')
        
    def txt_saveMore(self):
        try:
            txtFile = open('data.txt', 'a')
            strText = self.__ui.textBrowser.toPlainText()          
            txtFile.write(strText)
            txtFile.close()
            QMessageBox.information(self, 'Tips', 'Succeed to save!')
        except:
            print('Failed tu save!')
            QMessageBox.warning(self, 'Tips', 'Failed to save!')   
    def txttocsv_save(self):
        try:
            output_dict = {}

            input_file = 'data.txt'
            output_file ='data.csv'
            with open(input_file, 'r') as f: # open file, input file name is the first argument
                # for each line in file, seperate it into key-value pairs 
                # and store them in a dict.
                for line in f:
                    if line[2] == '=':
                        key, value = line.strip().split('=')
                        if key in output_dict:
                            output_dict[key].append(float(value))
                        else:
                            output_dict[key] = [float(value)]
            # sort the dict according to the key
            my_dict= dict(sorted(output_dict.items()))


            with open(output_file, 'w') as f:
                # check output_file type
                if output_file[-3:] == 'csv':
                    delimiter = ','
                else:
                    delimiter = ' '

                # get key-value from dict and format
                # data according to delimiter
                for key, value in my_dict.items():
                    line = key + delimiter
                    for num in value:
                        line = line + str(num) + delimiter

                    f.write(line + '\n')
            f.close()

            QMessageBox.information(self, 'Save Tips', 'Succeed to save!')
        except:
            print('Failed tu save!')
            QMessageBox.warning(self, 'Save Tips', 'Failed to save!')

    #菜单栏Version/Support
    def version(self):
        QMessageBox.information(self, 'Version Infos', 'Author: MIEMIEMIE\nVersion: V3.0\nTime: 28.02.2023\n')
    def support(self):
        QMessageBox.information(self, 'Support Infos', 'Email:\nzechuan.chen@etit.tu-chemnitz.de\n')

    #Mode切换
    def mode_change(self):
        self.clear() 
        print('mode change')
        if self.__ui.comboBox_6.currentText()=='Open Circuit Potentiometry':  
            self.__ui.tabWidget.setCurrentIndex(0)
        elif self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':   
            self.__ui.tabWidget.setCurrentIndex(1)
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':   
            self.__ui.tabWidget.setCurrentIndex(2)
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':   
            self.__ui.tabWidget.setCurrentIndex(3)
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':   
            self.__ui.tabWidget.setCurrentIndex(4)
        elif self.__ui.comboBox_6.currentText()=='Electrochemical Impedance Spectroscopy':   
            self.__ui.tabWidget.setCurrentIndex(5)
    def mode_change2(self):
        if self.__ui.tabWidget.currentIndex()==0:
            self.__ui.comboBox_6.setCurrentIndex(0)
        elif self.__ui.tabWidget.currentIndex()==1:
            self.__ui.comboBox_6.setCurrentIndex(1)
        elif self.__ui.tabWidget.currentIndex()==2:
            self.__ui.comboBox_6.setCurrentIndex(3)
        elif self.__ui.tabWidget.currentIndex()==3:
            self.__ui.comboBox_6.setCurrentIndex(4)
        elif self.__ui.tabWidget.currentIndex()==4:
            self.__ui.comboBox_6.setCurrentIndex(5)
        elif self.__ui.tabWidget.currentIndex()==5:
            self.__ui.comboBox_6.setCurrentIndex(6)


###########################################Tab1功能20220828##########################################
    def K1_detection(self):
        pw = pg.plot()
        pw.setTitle("K+ Channel1", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S5)

    def K2_detection(self):
        pw = pg.plot()
        pw.setTitle("K+ Channel2", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S6)
    
    def Ca1_detection(self):
        pw = pg.plot()
        pw.setTitle("Ca2+ Channel1", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S4)

    def Ca2_detection(self):
        pw = pg.plot()
        pw.setTitle("Ca2+ Channel2", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S7)

    def Mg1_detection(self):
        pw = pg.plot()
        pw.setTitle("Mg2+ Channel1", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S3)

    def Mg2_detection(self):
        pw = pg.plot()
        pw.setTitle("Mg2+ Channel2", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S8)

    def Blank_detection(self):
        pw = pg.plot()
        pw.setTitle("Blank Channel", color='008080', size='12pt')   # 设置图表标题、颜色、字体大小        
        pw.setBackground('w')          # 背景色改为白色
        pw.showGrid(x=True, y=True)    # 显示表格线
        pw.setLabel("left", "voltage")        # 设置上下左右的label     
        pw.setLabel("bottom", "Time")       # 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
        #pw.setYRange(min=2,max=3) # 设置Y轴 刻度 范围
        curve = pw.plot(pen=pg.mkPen('b')) # 线条颜色
        curve.setData(self.S2)

    #least square curve fitting y=kx+b
    def LScurveFitting(self,x,y):
        sumx = 0.0
        sumy = 0.0
        sumx2 = 0.0
        sumy2 = 0.0
        sumxy = 0.0
        errorSquare = 0.0
        rSquare = 0.0
        n=len(y)
        for i in range(len(x)):
            sumx += x[i]
            sumy += y[i]
            sumx2 += x[i] * x[i]
            sumy2 += y[i] * y[i]
            sumxy += x[i] * y[i]
        f_k = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
        f_b = (sumy * sumx2 - sumx * sumxy) / (n * sumx2 - sumx * sumx)
        
        for i in range(len(y)):
            errorSquare += (y[i]-(f_k*x[i]+f_b))*(y[i]-(f_k*x[i]+f_b))  #误差Q方,越小误差越小

        rSquare = (n * sumxy - sumx * sumy) * (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx) / (n * sumy2 - sumy * sumy) #R方,决定系数越接近1越准确
        return f_k,f_b,rSquare

    def constant_set(self):
        if self.__ui.comboBox_8.currentText()=='c_mg1': 
            try:
                self.c_mg1 = self.__ui.lineEdit_3.text()  
                self.c_mg1 = float(self.c_mg1)
                print(self.c_mg1) 
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='c_mg2':
            try:
                self.c_mg2 = self.__ui.lineEdit_3.text()
                self.c_mg2 = float(self.c_mg2)
                print(self.c_mg2)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mg1':
            try:
                self.k_mg1 = self.__ui.lineEdit_3.text() 
                self.k_mg1 = float(self.k_mg1)
                print(self.k_mg1)  
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mg2':
            try:
                self.k_mg2 = self.__ui.lineEdit_3.text()
                self.k_mg2 = float(self.k_mg2)
                print(self.k_mg2)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mgk1':
            try:
                self.k_mgk1 = self.__ui.lineEdit_3.text()
                self.k_mgk1 = float(self.k_mgk1)
                print(self.k_mgk1)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mgk2':
            try:
                self.k_mgk2 = self.__ui.lineEdit_3.text()
                self.k_mgk2 = float(self.k_mgk2)
                print(self.k_mgk2)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mgca1':
            try:
                self.k_mgca1 = self.__ui.lineEdit_3.text()
                self.k_mgca1 = float(self.k_mgca1)
                print(self.k_mgca1)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        elif self.__ui.comboBox_8.currentText()=='k_mgca2':
            try:
                self.k_mgca2 = self.__ui.lineEdit_3.text()
                self.k_mgca2 = float(self.k_mgca2)
                print(self.k_mgca2)
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
        self.__ui.lineEdit_3.setText('') 
 
    def curve_set(self):
        if self.__ui.comboBox_7.currentText()=='k1_data': 
            try:
                ion_data = self.__ui.lineEdit_2.text()  
                ion_data = ion_data.split(',')
                #print(ion_data)
                for i in range(len(ion_data)):
                    ion_data[i] = float(ion_data[i]) 
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
            self.__ui.lineEdit_2.setText('') 
            #print(ion_data)
            self.k1_funtion_kb=self.LScurveFitting(range(1,len(ion_data)+1),ion_data)

        elif self.__ui.comboBox_7.currentText()=='k2_data':
            try:
                ion_data = self.__ui.lineEdit_2.text()  
                ion_data = ion_data.split(',')
                #print(ion_data)
                for i in range(len(ion_data)):
                    ion_data[i] = float(ion_data[i]) 
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
            self.__ui.lineEdit_2.setText('') 
            #print(ion_data)
            self.k2_funtion_kb=self.LScurveFitting(range(1,len(ion_data)+1),ion_data)
        
        elif self.__ui.comboBox_7.currentText()=='ca1_data':
            try:
                ion_data = self.__ui.lineEdit_2.text()  
                ion_data = ion_data.split(',')
                #print(ion_data)
                for i in range(len(ion_data)):
                    ion_data[i] = float(ion_data[i]) 
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
            self.__ui.lineEdit_2.setText('') 
            #print(ion_data)
            self.ca1_funtion_kb=self.LScurveFitting(range(1,len(ion_data)+1),ion_data)

        elif self.__ui.comboBox_7.currentText()=='ca2_data':
            try:
                ion_data = self.__ui.lineEdit_2.text()  
                ion_data = ion_data.split(',')
                #print(ion_data)
                for i in range(len(ion_data)):
                    ion_data[i] = float(ion_data[i]) 
            except:
                QMessageBox.information(self, 'Warning', 'Please input numbers!')
            self.__ui.lineEdit_2.setText('') 
            #print(ion_data)
            self.ca2_funtion_kb=self.LScurveFitting(range(1,len(ion_data)+1),ion_data)
        
        print(self.k1_funtion_kb)
        print(self.k2_funtion_kb)
        print(self.ca1_funtion_kb)
        print(self.ca2_funtion_kb)  

####################Voltammetry#######################################################
    def parameter_E_begin(self): 
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            self.E_begin = self.__ui.lineEdit_4.text()
            self.send_lindEdit('E_begin'+self.E_begin+'\r\n')           
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':   
            self.E_begin = self.__ui.lineEdit_19.text()
            self.send_lindEdit('E_begin'+self.E_begin+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':   
            self.E_begin = self.__ui.lineEdit_27.text()
            self.send_lindEdit('E_begin'+self.E_begin+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':   
            self.E_begin = self.__ui.lineEdit_34.text()
            self.send_lindEdit('E_begin'+self.E_begin+'\r\n')
    def parameter_E_end(self): 
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            self.E_end = self.__ui.lineEdit_5.text()  
            self.send_lindEdit('E_end'+self.E_end+'\r\n')           
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':   
            self.E_end = self.__ui.lineEdit_18.text()
            self.send_lindEdit('E_end'+self.E_end+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':   
            self.E_end = self.__ui.lineEdit_25.text()
            self.send_lindEdit('E_end'+self.E_end+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':   
            self.E_end = self.__ui.lineEdit_31.text()
            self.send_lindEdit('E_end'+self.E_end+'\r\n')
    def parameter_E_step(self):
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            self.E_step = self.__ui.lineEdit_6.text()  
            self.send_lindEdit('E_step'+self.E_step+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':
            self.E_step = self.__ui.lineEdit_17.text()
            self.send_lindEdit('E_step'+self.E_step+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':   
            self.E_step = self.__ui.lineEdit_23.text()
            self.send_lindEdit('E_step'+self.E_step+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':   
            self.E_step = self.__ui.lineEdit_29.text()
            self.send_lindEdit('E_step'+self.E_step+'\r\n')       
    def parameter_E_scanrate(self):
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            self.E_scanrate = self.__ui.lineEdit_7.text()  
            self.send_lindEdit('E_scanrate'+self.E_scanrate+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':
            self.E_scanrate = self.__ui.lineEdit_16.text()
            self.send_lindEdit('E_scanrate'+self.E_scanrate+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':   
            self.E_scanrate = self.__ui.lineEdit_33.text()
            self.send_lindEdit('E_scanrate'+self.E_scanrate+'\r\n')   
    def parameter_E_numofscan(self):
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            self.E_numofscan = self.__ui.lineEdit_8.text()  
            self.send_lindEdit('E_numofscan'+self.E_numofscan+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':   
            self.E_numofscan = self.__ui.lineEdit_20.text()
            self.send_lindEdit('E_numofscan'+self.E_numofscan+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':   
            self.E_numofscan = self.__ui.lineEdit_26.text()
            self.send_lindEdit('E_numofscan'+self.E_numofscan+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry': 
            self.E_numofscan = self.__ui.lineEdit_30.text()
            self.send_lindEdit('E_numofscan'+self.E_numofscan+'\r\n')
    def set_current(self):
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry' or self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':
            if self.__ui.comboBox_9.currentText()=='10uA':  
                self.send_lindEdit('TMUX_10k'+'\r\n')
            elif self.__ui.comboBox_9.currentText()=='1uA':
                self.send_lindEdit('TMUX_100k'+'\r\n')
            elif self.__ui.comboBox_9.currentText()=='100uA':
                self.send_lindEdit('TMUX_1k'+'\r\n')
            elif self.__ui.comboBox_9.currentText()=='1mA':
                self.send_lindEdit('TMUX_100'+'\r\n')
        if self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':
            if self.__ui.comboBox_13.currentText()=='10uA':  
                self.send_lindEdit('TMUX_10k'+'\r\n')
            elif self.__ui.comboBox_13.currentText()=='1uA':
                self.send_lindEdit('TMUX_100k'+'\r\n')
            elif self.__ui.comboBox_13.currentText()=='100uA':
                self.send_lindEdit('TMUX_1k'+'\r\n')
            elif self.__ui.comboBox_13.currentText()=='1mA':
                self.send_lindEdit('TMUX_100'+'\r\n')
        if self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':
            if self.__ui.comboBox_14.currentText()=='10uA':  
                self.send_lindEdit('TMUX_10k'+'\r\n')
            elif self.__ui.comboBox_14.currentText()=='1uA':
                self.send_lindEdit('TMUX_100k'+'\r\n')
            elif self.__ui.comboBox_14.currentText()=='100uA':
                self.send_lindEdit('TMUX_1k'+'\r\n')
            elif self.__ui.comboBox_14.currentText()=='1mA':
                self.send_lindEdit('TMUX_100'+'\r\n')
        if self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':
            if self.__ui.comboBox_15.currentText()=='10uA':  
                self.send_lindEdit('TMUX_10k'+'\r\n')
            elif self.__ui.comboBox_15.currentText()=='1uA':
                self.send_lindEdit('TMUX_100k'+'\r\n')
            elif self.__ui.comboBox_15.currentText()=='100uA':
                self.send_lindEdit('TMUX_1k'+'\r\n')
            elif self.__ui.comboBox_15.currentText()=='1mA':
                self.send_lindEdit('TMUX_100'+'\r\n')
    def start_CV_LSV(self):
        if self.__ui.comboBox_6.currentText()=='Cyclic Voltammetry': 
            self.send_lindEdit('MODE 3'+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Linear Sweep Voltammetry':  
            self.send_lindEdit('MODE 2'+'\r\n')
    def parameter_E_pulse(self):       
        if self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':
            self.E_pulse = self.__ui.lineEdit_22.text()  
            self.send_lindEdit('E_pulse'+self.E_pulse+'\r\n')        
    def parameter_E_Tpulse(self):   
        if self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry':  
            self.E_Tpulse = self.__ui.lineEdit_21.text()  
            self.send_lindEdit('E_Tpulse'+self.E_Tpulse+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry':  
            self.E_Tpulse = self.__ui.lineEdit_32.text()  
            self.send_lindEdit('E_Tpulse'+self.E_Tpulse+'\r\n')
    def parameter_E_amplitude(self):        
        if self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry': 
            self.E_amplitude = self.__ui.lineEdit_24.text()  
            self.send_lindEdit('E_amplitude'+self.E_amplitude+'\r\n')
    def parameter_E_frequency(self):   
        if self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry':
            self.E_frequency = self.__ui.lineEdit_28.text()  
            self.send_lindEdit('E_frequency'+self.E_frequency+'\r\n')
    def start_Other(self):
        if self.__ui.comboBox_6.currentText()=='Differential Pulse Voltammetry': 
            self.send_lindEdit('MODE 4'+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Square Wave Voltammetry': 
            self.send_lindEdit('MODE 5'+'\r\n')
        elif self.__ui.comboBox_6.currentText()=='Normal Pulse Voltammetry': 
            self.send_lindEdit('MODE 6'+'\r\n')  

########Electrochemical Impedance Spectroscopy########################################
    def parameter_P_startFREQ(self):
        self.P_startFREQ = self.__ui.lineEdit_36.text()
        self.send_lindEdit('P_startFREQ'+self.P_startFREQ+'\r\n')
    def parameter_P_freqINCR(self):
        self.P_freqINCR = self.__ui.lineEdit_35.text()
        self.send_lindEdit('P_freqINCR'+self.P_freqINCR+'\r\n')
    def parameter_P_numINCR(self):
        self.P_numINCR = self.__ui.lineEdit_37.text()
        self.send_lindEdit('P_numINCR'+self.P_numINCR+'\r\n')
    def parameter_P_refRESIST(self):
        self.P_refRESIST = self.__ui.lineEdit_38.text()
        self.send_lindEdit('P_refRESIST'+self.P_refRESIST+'\r\n')
    def parameter_R_refNum(self):
        self.R_refNum = self.__ui.lineEdit_39.text()
        self.send_lindEdit('R_refNum'+self.R_refNum+'\r\n')
    def parameter_R_unkNum(self):
        self.R_unkNum = self.__ui.lineEdit_40.text()
        self.send_lindEdit('R_unkNum'+self.R_unkNum+'\r\n')
    def eis_mode(self):
        if self.__ui.comboBox_16.currentText()=='Single':  
            self.send_lindEdit('MODE B'+'\r\n')
        elif self.__ui.comboBox_16.currentText()=='Multiple':
            self.send_lindEdit('MODE C'+'\r\n')
    def start_EIS(self):
        self.send_lindEdit('START'+'\r\n')
    def set_EIS_graph(self):       
        if self.__ui.comboBox_10.currentIndex()==0: 
            self.__ui.graphicsView.clear()
            self.__ui.graphicsView.setLabel("left", "Z_im")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "Z_re")
            self.__ui.graphicsView.plot(self.R1,self.I1,pen=pg.mkPen(color=(125,120,120),width=3))
        elif self.__ui.comboBox_10.currentIndex()==1:
            self.__ui.graphicsView.clear()
            self.__ui.graphicsView.setLabel("left", "Z_re")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "f(hz)")
            self.__ui.graphicsView.plot(self.R1,pen=pg.mkPen(color=(255,165,0),width=3)) 
        elif self.__ui.comboBox_10.currentIndex()==2:
            self.__ui.graphicsView.clear()
            self.__ui.graphicsView.setLabel("left", "Z_im")# 第一个参数 只能是 'left', 'bottom', 'right', or 'top'
            self.__ui.graphicsView.setLabel("bottom", "f(hz)")
            self.__ui.graphicsView.plot(self.I1,pen=pg.mkPen(color=(255,0,255),width=3)) 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mymainWindow = MyMainWindow()
    mymainWindow.show()
    sys.exit(app.exec())
