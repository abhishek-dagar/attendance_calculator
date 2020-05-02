# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
import time
import threading
from Student import Student
stylesheet_data='''

QWidget{
background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383736, stop: 1 #131415);
}
QLineEdit{
background:transparent;
border:none;
color:white;
border-bottom:3px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 red, stop: 1 red);
}
QPushButton{
    background:transparent;
    background-color:red;
    color:white;
    border-width:2px;
    border-radius:15px;
    }

'''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.count=False
        fnt = QtGui.QFont('Arial', 19)
        fnt1 = QtGui.QFont('Arial', 14)
        self.MainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 650)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setStyleSheet('''background-image:url('backimg.png')''')
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(29, 75, 541, 521))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383736, stop: 1 #131415); border-radius:25")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 490, 181, 61))
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.on_click())
        self.pushButton.setFont(fnt1)


        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setObjectName("name")
        self.name.setGeometry(QtCore.QRect(110, 190, 400, 50))
        self.name.setPlaceholderText('Username')
        self.name.setFont(fnt)


        self.passw = QtWidgets.QLineEdit(self.centralwidget)
        self.passw.setObjectName("pass")
        self.passw.setGeometry(QtCore.QRect(110, 290, 400, 50))
        self.passw.setPlaceholderText('Password')
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passw.setFont(fnt)


    
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(250, 20, 101, 81))
        self.photo.setObjectName("photo")
        self.photo.setStyleSheet("background:transparent;background-image:url('images.png')")


        self.show_result = QtWidgets.QLabel(self.centralwidget)
        self.show_result.setGeometry(QtCore.QRect(90, 390, 400, 71))
        self.show_result.setObjectName("show_result")
        MainWindow.setCentralWidget(self.centralwidget)
        self.show_result.setFont(fnt)
        self.show_result.setStyleSheet("background:transparent;color:white;")

        #self.vbox = QtWidgets.QVBoxLayout()


        self.name.raise_()
        self.passw.raise_()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendace Calculator"))
        self.pushButton.setText(_translate("MainWindow", "LOGIN"))


    
        
    def on_click(self):
        if self.name.text()!='':
            if self.passw.text()!='':
                self.show_result.setText("conecting to server")
        if self.name.text()!='' and self.passw.text()!='':
            
            result=self.main(self.name.text(),self.passw.text())
            if result=='logged in':
                self.Window=QtWidgets.QMainWindow()
                self.ui = show_attendance(self.Window,self.name.text(),self.passw.text())
                self.Window.setStyleSheet(stylesheet_data)
                self.Window.show()
                self.MainWindow.close()
            else:
                print(result)
        else:
            self.show_result.setText("Please enter you Username and pass word")
    def main(self,username, password, retry=0):
        if retry:
            print('retrying: {}'.format(retry))
            time.sleep(5)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36"}

        # opts = webdriverOptions()
        # options.add_argument("--headless") # Runs Chrome in headless mode.
        attendance_url = 'http://app.bmiet.net/student/attendance/view'
        url = 'http://app.bmiet.net/student/login'
        form_action_url = 'http://app.bmiet.net/student/student-login'
        login_data = {'username': username,
                      'password': password}
        student_data = Student()  # Student class instance

        with requests.Session() as s:
            try:
                r = s.get(url, headers=headers)
            except:
                return None#self.main(username, password, retry + 1)
            #self.show_result.setText('    connected to the server')
            soup = BeautifulSoup(r.text, 'html5lib')
            login_data['_token'] = soup.find(
                'input', attrs={'name': '_token'})['value']
            r = s.post(form_action_url, data=login_data, headers=headers)

            # To extract student name from the dashboard page
            page = "".join(line.strip() for line in r.text.split("\n"))
            soup = BeautifulSoup(page, 'html5lib')
            try:
                student_data.name = soup.find(class_="user-panel").find('p').text
                self.show_result.setText('   logged in')
                return 'logged in'
            except AttributeError:
                self.show_result.setText('    wrong Credentials')
                return 'not logging'
        

class show_attendance(object):
    def __init__(self, MainWindow,name,password):
        self.MainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 750)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        fnt = QtGui.QFont('Arial', 19)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 771, 531))
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet("background-color:white;color:black;")

        self.Window=QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Window)
        self.Window.setStyleSheet(stylesheet_data)
        

        self.show_result = QtWidgets.QLabel(self.centralwidget)
        self.show_result.setGeometry(QtCore.QRect(10, 555, 771, 121))
        self.show_result.setObjectName("show_result")
        MainWindow.setCentralWidget(self.centralwidget)
        self.show_result.setFont(fnt)
        self.show_result.setStyleSheet("background:transparent;color:white;")        

        self.perform(name,password)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 700, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.on_click())
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "result"))
        self.pushButton.setText(_translate("MainWindow", "Logout"))
    def on_click(self):
        self.Window.show()
        self.MainWindow.close()

    def perform(self,name, password):
        student = self.main(name, password)
        if student is not None:
            attendance_info = student.attendance.get_full_information()
            subject_info,sub_name=student.subjects.all_subject_information()
            sub_name.sort()
            self.subject_info=subject_info
            self.sub_name=sub_name
            self.tableView.setRowCount(len(sub_name))
            self.tableView.setColumnCount(4)
            self.tableView.verticalHeader().setVisible(False)
            for i in range(len(sub_name)):
                self.tableView.setItem(i,0,QtWidgets.QTableWidgetItem(sub_name[i]))
                self.tableView.setItem(i,1,QtWidgets.QTableWidgetItem(str(subject_info[sub_name[i]]['present'])))
                self.tableView.setItem(i,2,QtWidgets.QTableWidgetItem(str(subject_info[sub_name[i]]['absent'])))
                self.tableView.setItem(i,3,QtWidgets.QTableWidgetItem(str(round(subject_info[sub_name[i]]['percentage'],2))))

            self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tableView.setHorizontalHeaderLabels(("Subject Name;Present;Absent;Percentage").split(";"));

            
            if attendance_info['attend'] == 0:
                self.show_result.setText("\tName:"+student.name+"\n\tAttendance: {}".format(round(attendance_info['percentage'],2))+"%\n\tBunk: {}".format(attendance_info['bunk']))
            else:
                self.show_result.setText("\tName:"+student.name+"\n\tAttendance: {}".format(round(attendance_info['percentage'],2))+"%\n\tAttend: {}".format(attendance_info['attend']))


    def scapAttendance(self,s, headers, attendance_url):
        r = s.get(attendance_url, headers=headers)
        page = "".join(line.strip() for line in r.text.split("\n"))
        soup = BeautifulSoup(page, 'html5lib')
        dataset = []
        table = soup.find_all('tbody')[1]
        rows = table.find_all('tr')
        rows.pop()
        for row in rows:
            row = row.find_all('td')
            data_row = []
            for cell in row:
                data_row.append(cell.text)
            dataset.append(data_row)
        try:
            attendance_url = soup.find('a', attrs={'rel': 'next'})['href']
        except TypeError:
            pass
        return dataset

    def main(self,username, password, retry=0):
        if retry:
            print('retrying: {}'.format(retry))
            time.sleep(5)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36"}

        # opts = webdriverOptions()
        # options.add_argument("--headless") # Runs Chrome in headless mode.
        attendance_url = 'http://app.bmiet.net/student/attendance/view'
        url = 'http://app.bmiet.net/student/login'
        form_action_url = 'http://app.bmiet.net/student/student-login'
        login_data = {'username': username,
                      'password': password}
        student_data = Student()  # Student class instance

        with requests.Session() as s:
            try:
                r = s.get(url, headers=headers)
            except:
                return None#self.main(username, password, retry + 1)
            #self.show_result.setText('    connected to the server')
            soup = BeautifulSoup(r.text, 'html5lib')
            login_data['_token'] = soup.find(
                'input', attrs={'name': '_token'})['value']
            r = s.post(form_action_url, data=login_data, headers=headers)

            # To extract student name from the dashboard page
            page = "".join(line.strip() for line in r.text.split("\n"))
            soup = BeautifulSoup(page, 'html5lib')
            try:
                student_data.name = soup.find(class_="user-panel").find('p').text
                #self.show_result.setText('   logged in')
            except AttributeError:
                #self.show_result.setText('    wrong Credentials')
                return None
            # # # # # # # # #

            dataset = []
            count = 0
            while True:
                r = s.get(attendance_url, headers=headers)
                page = "".join(line.strip() for line in r.text.split("\n"))
                soup = BeautifulSoup(page, 'html5lib')

                table = soup.find_all('tbody')[1]
                rows = table.find_all('tr')
                rows.pop()
                for row in rows:
                    row = row.find_all('td')
                    data_row = []
                    for cell in row:
                        data_row.append(cell.text)
                    dataset.append(data_row)
                    count += 1
                try:
                    attendance_url = soup.find('a', attrs={'rel': 'next'})['href']
                except TypeError:
                    break
            student_data.attendance_sheet(dataset)
        return student_data



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setStyleSheet(stylesheet_data)
    MainWindow.show()
    sys.exit(app.exec_())

