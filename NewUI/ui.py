# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 723)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(parent=self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(230, 60, 571, 451))
        self.graphicsView.setObjectName("graphicsView")
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 520, 191, 81))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 60, 191, 401))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 54, 16))
        self.label.setStyleSheet("color:rgb(0, 0, 127)")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 10, 51, 20))
        self.label_2.setStyleSheet("color:rgb(0, 0, 127)")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 10, 61, 16))
        self.label_3.setStyleSheet("color:rgb(0, 0, 127)")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 10, 61, 20))
        self.label_4.setStyleSheet("color:rgb(0, 0, 127)")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(530, 10, 54, 16))
        self.label_5.setStyleSheet("color:rgb(0, 0, 127)")
        self.label_5.setObjectName("label_5")
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 10, 68, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(310, 10, 68, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(450, 10, 68, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_4 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(180, 10, 68, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_5 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_5.setGeometry(QtCore.QRect(580, 10, 68, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(660, 10, 61, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(730, 10, 61, 24))
        self.pushButton_2.setStyleSheet("color: rgb(0, 0, 255)")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 630, 75, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 490, 51, 24))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(140, 490, 51, 24))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(80, 490, 51, 24))
        self.pushButton_6.setObjectName("pushButton_6")
        self.checkBox = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 630, 79, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 470, 91, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 610, 51, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 40, 141, 16))
        self.label_6.setStyleSheet("color:rgb(100,100,100)")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(160, 610, 54, 16))
        self.label_7.setObjectName("label_7")
        self.checkBox_3 = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 610, 79, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.comboBox_6 = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox_6.setGeometry(QtCore.QRect(230, 40, 311, 22))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(230, 520, 561, 181))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(0, 0, 81, 24))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(90, 0, 81, 24))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 30, 81, 24))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_10.setGeometry(QtCore.QRect(90, 30, 81, 24))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_11.setGeometry(QtCore.QRect(0, 60, 81, 24))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_12.setGeometry(QtCore.QRect(90, 60, 81, 24))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_13.setGeometry(QtCore.QRect(0, 90, 81, 24))
        self.pushButton_13.setObjectName("pushButton_13")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(272, 10, 281, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_9 = QtWidgets.QLabel(parent=self.tab)
        self.label_9.setGeometry(QtCore.QRect(270, 60, 131, 20))
        self.label_9.setStyleSheet("color:rgb(100,100,250)")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(parent=self.tab)
        self.label_10.setGeometry(QtCore.QRect(270, 80, 131, 20))
        self.label_10.setStyleSheet("color:rgb(100,100,250)")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(parent=self.tab)
        self.label_11.setGeometry(QtCore.QRect(270, 100, 131, 16))
        self.label_11.setStyleSheet("color:rgb(100,100,250)")
        self.label_11.setObjectName("label_11")
        self.comboBox_7 = QtWidgets.QComboBox(parent=self.tab)
        self.comboBox_7.setGeometry(QtCore.QRect(200, 10, 71, 22))
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.label_12 = QtWidgets.QLabel(parent=self.tab)
        self.label_12.setGeometry(QtCore.QRect(400, 60, 151, 20))
        self.label_12.setStyleSheet("color:rgb(100,10,250)")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(parent=self.tab)
        self.label_13.setGeometry(QtCore.QRect(400, 80, 151, 20))
        self.label_13.setStyleSheet("color:rgb(100,10,250)")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(parent=self.tab)
        self.label_14.setGeometry(QtCore.QRect(400, 100, 151, 16))
        self.label_14.setStyleSheet("color:rgb(100,10,250)")
        self.label_14.setObjectName("label_14")
        self.comboBox_8 = QtWidgets.QComboBox(parent=self.tab)
        self.comboBox_8.setGeometry(QtCore.QRect(200, 40, 71, 22))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(272, 40, 111, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_15 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.label_18.setObjectName("label_18")
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(90, 10, 61, 20))
        self.lineEdit_4.setFrame(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(90, 30, 61, 20))
        self.lineEdit_5.setFrame(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(90, 50, 61, 20))
        self.lineEdit_6.setFrame(True)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(100, 70, 61, 20))
        self.lineEdit_7.setFrame(True)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(100, 90, 61, 20))
        self.lineEdit_8.setFrame(True)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.comboBox_9 = QtWidgets.QComboBox(parent=self.tab_2)
        self.comboBox_9.setGeometry(QtCore.QRect(10, 110, 71, 22))
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.pushButton_14 = QtWidgets.QPushButton(parent=self.tab_2)
        self.pushButton_14.setGeometry(QtCore.QRect(90, 110, 81, 24))
        self.pushButton_14.setObjectName("pushButton_14")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.comboBox_13 = QtWidgets.QComboBox(parent=self.tab_3)
        self.comboBox_13.setGeometry(QtCore.QRect(10, 110, 71, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.label_30 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_30.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_30.setObjectName("label_30")
        self.lineEdit_16 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_16.setGeometry(QtCore.QRect(100, 70, 61, 20))
        self.lineEdit_16.setFrame(True)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.label_31 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_31.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_32.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_33.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.label_33.setObjectName("label_33")
        self.pushButton_23 = QtWidgets.QPushButton(parent=self.tab_3)
        self.pushButton_23.setGeometry(QtCore.QRect(90, 110, 81, 24))
        self.pushButton_23.setObjectName("pushButton_23")
        self.lineEdit_17 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_17.setGeometry(QtCore.QRect(90, 50, 61, 20))
        self.lineEdit_17.setFrame(True)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.label_34 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_34.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_34.setObjectName("label_34")
        self.lineEdit_18 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_18.setGeometry(QtCore.QRect(90, 30, 61, 20))
        self.lineEdit_18.setFrame(True)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.lineEdit_19 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_19.setGeometry(QtCore.QRect(90, 10, 61, 20))
        self.lineEdit_19.setFrame(True)
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_20 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_20.setGeometry(QtCore.QRect(100, 90, 61, 20))
        self.lineEdit_20.setFrame(True)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.label_35 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_35.setGeometry(QtCore.QRect(160, 30, 71, 16))
        self.label_35.setObjectName("label_35")
        self.lineEdit_21 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_21.setGeometry(QtCore.QRect(230, 30, 61, 20))
        self.lineEdit_21.setFrame(True)
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.label_36 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_36.setGeometry(QtCore.QRect(160, 10, 71, 16))
        self.label_36.setObjectName("label_36")
        self.lineEdit_22 = QtWidgets.QLineEdit(parent=self.tab_3)
        self.lineEdit_22.setGeometry(QtCore.QRect(230, 10, 61, 20))
        self.lineEdit_22.setFrame(True)
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.label_37 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_37.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_38.setGeometry(QtCore.QRect(160, 30, 101, 16))
        self.label_38.setObjectName("label_38")
        self.lineEdit_23 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_23.setGeometry(QtCore.QRect(90, 50, 61, 20))
        self.lineEdit_23.setFrame(True)
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.label_39 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_39.setGeometry(QtCore.QRect(160, 10, 101, 16))
        self.label_39.setObjectName("label_39")
        self.lineEdit_24 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_24.setGeometry(QtCore.QRect(250, 30, 61, 20))
        self.lineEdit_24.setFrame(True)
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.label_40 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_40.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_41.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_41.setObjectName("label_41")
        self.lineEdit_25 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_25.setGeometry(QtCore.QRect(90, 30, 61, 20))
        self.lineEdit_25.setFrame(True)
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.lineEdit_26 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_26.setGeometry(QtCore.QRect(100, 90, 61, 20))
        self.lineEdit_26.setFrame(True)
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.comboBox_14 = QtWidgets.QComboBox(parent=self.tab_4)
        self.comboBox_14.setGeometry(QtCore.QRect(10, 110, 71, 22))
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.label_42 = QtWidgets.QLabel(parent=self.tab_4)
        self.label_42.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_42.setObjectName("label_42")
        self.lineEdit_27 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_27.setGeometry(QtCore.QRect(90, 10, 61, 20))
        self.lineEdit_27.setFrame(True)
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.lineEdit_28 = QtWidgets.QLineEdit(parent=self.tab_4)
        self.lineEdit_28.setGeometry(QtCore.QRect(250, 10, 61, 20))
        self.lineEdit_28.setFrame(True)
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.pushButton_24 = QtWidgets.QPushButton(parent=self.tab_4)
        self.pushButton_24.setGeometry(QtCore.QRect(90, 110, 81, 24))
        self.pushButton_24.setObjectName("pushButton_24")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.comboBox_15 = QtWidgets.QComboBox(parent=self.tab_5)
        self.comboBox_15.setGeometry(QtCore.QRect(10, 110, 71, 22))
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.label_43 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_43.setGeometry(QtCore.QRect(160, 10, 101, 16))
        self.label_43.setObjectName("label_43")
        self.lineEdit_29 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_29.setGeometry(QtCore.QRect(90, 50, 61, 20))
        self.lineEdit_29.setFrame(True)
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.label_44 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_44.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_44.setObjectName("label_44")
        self.lineEdit_30 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_30.setGeometry(QtCore.QRect(100, 90, 61, 20))
        self.lineEdit_30.setFrame(True)
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.lineEdit_31 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_31.setGeometry(QtCore.QRect(90, 30, 61, 20))
        self.lineEdit_31.setFrame(True)
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.label_45 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_45.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_46.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_47.setGeometry(QtCore.QRect(160, 30, 101, 16))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(parent=self.tab_5)
        self.label_48.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.label_48.setObjectName("label_48")
        self.lineEdit_32 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_32.setGeometry(QtCore.QRect(250, 10, 61, 20))
        self.lineEdit_32.setFrame(True)
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.lineEdit_33 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_33.setGeometry(QtCore.QRect(250, 30, 61, 20))
        self.lineEdit_33.setFrame(True)
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.lineEdit_34 = QtWidgets.QLineEdit(parent=self.tab_5)
        self.lineEdit_34.setGeometry(QtCore.QRect(90, 10, 61, 20))
        self.lineEdit_34.setFrame(True)
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.pushButton_25 = QtWidgets.QPushButton(parent=self.tab_5)
        self.pushButton_25.setGeometry(QtCore.QRect(90, 110, 81, 24))
        self.pushButton_25.setObjectName("pushButton_25")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_49 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_49.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_49.setObjectName("label_49")
        self.lineEdit_35 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_35.setGeometry(QtCore.QRect(90, 30, 61, 20))
        self.lineEdit_35.setFrame(True)
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.label_50 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_50.setGeometry(QtCore.QRect(10, 70, 101, 16))
        self.label_50.setObjectName("label_50")
        self.lineEdit_36 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_36.setGeometry(QtCore.QRect(90, 10, 61, 20))
        self.lineEdit_36.setFrame(True)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.lineEdit_37 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_37.setGeometry(QtCore.QRect(90, 50, 61, 20))
        self.lineEdit_37.setFrame(True)
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.lineEdit_38 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_38.setGeometry(QtCore.QRect(90, 70, 61, 20))
        self.lineEdit_38.setFrame(True)
        self.lineEdit_38.setObjectName("lineEdit_38")
        self.label_51 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_51.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_52.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_52.setObjectName("label_52")
        self.lineEdit_39 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_39.setGeometry(QtCore.QRect(90, 90, 61, 20))
        self.lineEdit_39.setFrame(True)
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.label_53 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_53.setGeometry(QtCore.QRect(10, 90, 81, 16))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(parent=self.tab_6)
        self.label_54.setGeometry(QtCore.QRect(10, 110, 81, 16))
        self.label_54.setObjectName("label_54")
        self.lineEdit_40 = QtWidgets.QLineEdit(parent=self.tab_6)
        self.lineEdit_40.setGeometry(QtCore.QRect(90, 110, 61, 20))
        self.lineEdit_40.setFrame(True)
        self.lineEdit_40.setObjectName("lineEdit_40")
        self.comboBox_16 = QtWidgets.QComboBox(parent=self.tab_6)
        self.comboBox_16.setGeometry(QtCore.QRect(180, 10, 71, 22))
        self.comboBox_16.setObjectName("comboBox_16")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.pushButton_26 = QtWidgets.QPushButton(parent=self.tab_6)
        self.pushButton_26.setGeometry(QtCore.QRect(260, 10, 81, 24))
        self.pushButton_26.setObjectName("pushButton_26")
        self.comboBox_10 = QtWidgets.QComboBox(parent=self.tab_6)
        self.comboBox_10.setGeometry(QtCore.QRect(440, 10, 91, 22))
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.tabWidget.addTab(self.tab_6, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuInfo = QtWidgets.QMenu(parent=self.menubar)
        self.menuInfo.setObjectName("menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionVersion = QtGui.QAction(parent=MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionSupport = QtGui.QAction(parent=MainWindow)
        self.actionSupport.setObjectName("actionSupport")
        self.actionSave_as_CSV = QtGui.QAction(parent=MainWindow)
        self.actionSave_as_CSV.setObjectName("actionSave_as_CSV")
        self.menuFile.addAction(self.actionSave_as_CSV)
        self.menuInfo.addAction(self.actionVersion)
        self.menuInfo.addAction(self.actionSupport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MieUI"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Please enter the information, support Enter"))
        self.label.setText(_translate("MainWindow", "Port:"))
        self.label_2.setText(_translate("MainWindow", "Data bit:"))
        self.label_3.setText(_translate("MainWindow", "Parity bit:"))
        self.label_4.setText(_translate("MainWindow", "Baud rate:"))
        self.label_5.setText(_translate("MainWindow", "Stop bit:"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "8"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "7"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "6"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "5"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "N"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "E"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "O"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "M"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "115200"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "9600"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "2"))
        self.pushButton.setText(_translate("MainWindow", "Refresh"))
        self.pushButton_2.setText(_translate("MainWindow", "Open"))
        self.pushButton_3.setText(_translate("MainWindow", "Send"))
        self.pushButton_4.setText(_translate("MainWindow", "Clear"))
        self.pushButton_5.setText(_translate("MainWindow", "Save"))
        self.pushButton_6.setText(_translate("MainWindow", "Save+"))
        self.checkBox.setText(_translate("MainWindow", "HEX"))
        self.checkBox_2.setText(_translate("MainWindow", "HEX Display"))
        self.label_6.setText(_translate("MainWindow", "Send: 0 Receive: 0"))
        self.label_7.setText(_translate("MainWindow", "ms/time"))
        self.checkBox_3.setText(_translate("MainWindow", "Automatic"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "Open Circuit Potentiometry"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "Cyclic Voltammetry"))
        self.comboBox_6.setItemText(2, _translate("MainWindow", "Linear Sweep Voltammetry"))
        self.comboBox_6.setItemText(3, _translate("MainWindow", "Differential Pulse Voltammetry"))
        self.comboBox_6.setItemText(4, _translate("MainWindow", "Square Wave Voltammetry"))
        self.comboBox_6.setItemText(5, _translate("MainWindow", "Normal Pulse Voltammetry"))
        self.comboBox_6.setItemText(6, _translate("MainWindow", "Electrochemical Impedance Spectroscopy"))
        self.pushButton_7.setText(_translate("MainWindow", "S5: K1"))
        self.pushButton_8.setText(_translate("MainWindow", "S6: K2"))
        self.pushButton_9.setText(_translate("MainWindow", "S4: Ca1"))
        self.pushButton_10.setText(_translate("MainWindow", "S7: Ca2"))
        self.pushButton_11.setText(_translate("MainWindow", "S3: Mg1"))
        self.pushButton_12.setText(_translate("MainWindow", "S8: Mg2"))
        self.pushButton_13.setText(_translate("MainWindow", "S2: Blank"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "The separator is \",\" confirm is \"Enter\"  "))
        self.label_9.setText(_translate("MainWindow", "K1: 0mol/L"))
        self.label_10.setText(_translate("MainWindow", "Ca1: 0mol/L"))
        self.label_11.setText(_translate("MainWindow", "Mg1: 0mol/L"))
        self.comboBox_7.setItemText(0, _translate("MainWindow", "k1_data"))
        self.comboBox_7.setItemText(1, _translate("MainWindow", "k2_data"))
        self.comboBox_7.setItemText(2, _translate("MainWindow", "ca1_data"))
        self.comboBox_7.setItemText(3, _translate("MainWindow", "ca2_data"))
        self.label_12.setText(_translate("MainWindow", "K2: 0mol/L"))
        self.label_13.setText(_translate("MainWindow", "Ca2: 0mol/L"))
        self.label_14.setText(_translate("MainWindow", "Mg2: 0mol/L"))
        self.comboBox_8.setItemText(0, _translate("MainWindow", "c_mg1"))
        self.comboBox_8.setItemText(1, _translate("MainWindow", "k_mg1"))
        self.comboBox_8.setItemText(2, _translate("MainWindow", "k_mgk1"))
        self.comboBox_8.setItemText(3, _translate("MainWindow", "k_mgca1"))
        self.comboBox_8.setItemText(4, _translate("MainWindow", "c_mg2"))
        self.comboBox_8.setItemText(5, _translate("MainWindow", "k_mg2"))
        self.comboBox_8.setItemText(6, _translate("MainWindow", "k_mgk2"))
        self.comboBox_8.setItemText(7, _translate("MainWindow", "k_mgca2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "OCP"))
        self.label_8.setText(_translate("MainWindow", "E_begin(mV)"))
        self.label_15.setText(_translate("MainWindow", "E_end(mV)"))
        self.label_16.setText(_translate("MainWindow", "E_step(mV)"))
        self.label_17.setText(_translate("MainWindow", "Scanrate(mV/s)"))
        self.label_18.setText(_translate("MainWindow", "NumberOfScan"))
        self.comboBox_9.setItemText(0, _translate("MainWindow", "10uA"))
        self.comboBox_9.setItemText(1, _translate("MainWindow", "1uA"))
        self.comboBox_9.setItemText(2, _translate("MainWindow", "100uA"))
        self.comboBox_9.setItemText(3, _translate("MainWindow", "1mA"))
        self.pushButton_14.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "CV/LSV"))
        self.comboBox_13.setItemText(0, _translate("MainWindow", "10uA"))
        self.comboBox_13.setItemText(1, _translate("MainWindow", "1uA"))
        self.comboBox_13.setItemText(2, _translate("MainWindow", "100uA"))
        self.comboBox_13.setItemText(3, _translate("MainWindow", "1mA"))
        self.label_30.setText(_translate("MainWindow", "E_begin(mV)"))
        self.label_31.setText(_translate("MainWindow", "E_end(mV)"))
        self.label_32.setText(_translate("MainWindow", "Scanrate(mV/s)"))
        self.label_33.setText(_translate("MainWindow", "NumberOfScan"))
        self.pushButton_23.setText(_translate("MainWindow", "Start"))
        self.label_34.setText(_translate("MainWindow", "E_step(mV)"))
        self.label_35.setText(_translate("MainWindow", "T_pulse(ms)"))
        self.label_36.setText(_translate("MainWindow", "E_pulse(mV)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "DPV"))
        self.label_37.setText(_translate("MainWindow", "E_end(mV)"))
        self.label_38.setText(_translate("MainWindow", "Amplitude(mV)"))
        self.label_39.setText(_translate("MainWindow", "Frequency(Hz)"))
        self.label_40.setText(_translate("MainWindow", "NumberOfScan"))
        self.label_41.setText(_translate("MainWindow", "E_step(mV)"))
        self.comboBox_14.setItemText(0, _translate("MainWindow", "10uA"))
        self.comboBox_14.setItemText(1, _translate("MainWindow", "1uA"))
        self.comboBox_14.setItemText(2, _translate("MainWindow", "100uA"))
        self.comboBox_14.setItemText(3, _translate("MainWindow", "1mA"))
        self.label_42.setText(_translate("MainWindow", "E_begin(mV)"))
        self.pushButton_24.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "SWV"))
        self.comboBox_15.setItemText(0, _translate("MainWindow", "10uA"))
        self.comboBox_15.setItemText(1, _translate("MainWindow", "1uA"))
        self.comboBox_15.setItemText(2, _translate("MainWindow", "100uA"))
        self.comboBox_15.setItemText(3, _translate("MainWindow", "1mA"))
        self.label_43.setText(_translate("MainWindow", "T_pulse(ms)"))
        self.label_44.setText(_translate("MainWindow", "E_step(mV)"))
        self.label_45.setText(_translate("MainWindow", "E_end(mV)"))
        self.label_46.setText(_translate("MainWindow", "E_begin(mV)"))
        self.label_47.setText(_translate("MainWindow", "Scanrate(mV/s)"))
        self.label_48.setText(_translate("MainWindow", "NumberOfScan"))
        self.pushButton_25.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "NPV"))
        self.label_49.setText(_translate("MainWindow", "P_startFREQ"))
        self.label_50.setText(_translate("MainWindow", "P_refRESIST"))
        self.label_51.setText(_translate("MainWindow", "P_freqINCR"))
        self.label_52.setText(_translate("MainWindow", "P_numINCR"))
        self.label_53.setText(_translate("MainWindow", "R_refNum"))
        self.label_54.setText(_translate("MainWindow", "R_unkNum"))
        self.comboBox_16.setItemText(0, _translate("MainWindow", "-----"))
        self.comboBox_16.setItemText(1, _translate("MainWindow", "Single"))
        self.comboBox_16.setItemText(2, _translate("MainWindow", "Multiple"))
        self.pushButton_26.setText(_translate("MainWindow", "Start"))
        self.comboBox_10.setItemText(0, _translate("MainWindow", "Re(Z)-Im(Z)"))
        self.comboBox_10.setItemText(1, _translate("MainWindow", "f-Re(Z)"))
        self.comboBox_10.setItemText(2, _translate("MainWindow", "f-Im(Z)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "EIS"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionSupport.setText(_translate("MainWindow", "Support"))
        self.actionSave_as_CSV.setText(_translate("MainWindow", "Save as CSV"))
from pyqtgraph import PlotWidget