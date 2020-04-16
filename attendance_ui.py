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

QWidget
{
    background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383736, stop: 1 #131415);
}
QLineEdit{
color:white;
border-radius: 20px;
border:3px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #00BFFF, stop: 1 #00BFFF);
}


    QPushButton{
    background:transparent;
    background-color:#00BFFF;
    color:white;
    border: 3px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #00BFFF, stop: 1 #00BFFF);
    border-width:2px;
    }
'''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.count=False
        fnt = QtGui.QFont('Arial', 19)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setObjectName("name")
        self.name.setGeometry(QtCore.QRect(190, 190, 400, 50))
        self.name.setPlaceholderText('  Username')
        self.name.setFont(fnt)


        self.passw = QtWidgets.QLineEdit(self.centralwidget)
        self.passw.setObjectName("pass")
        self.passw.setGeometry(QtCore.QRect(190, 290, 400, 50))
        self.passw.setPlaceholderText('  Password')
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passw.setFont(fnt)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 490, 181, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("border-radius:15px;")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(330, 60, 101, 81))
        self.photo.setObjectName("photo")
        self.photo.setStyleSheet("background:transparent;background-image:url('images.png')")


        self.show_result = QtWidgets.QLabel(self.centralwidget)
        self.show_result.setGeometry(QtCore.QRect(0, 150, 800, 301))
        self.show_result.setObjectName("show_result")
        MainWindow.setCentralWidget(self.centralwidget)
        self.show_result.setFont(fnt)
        self.show_result.setStyleSheet("background:transparent;color:white;")
        self.pushButton.clicked.connect(lambda: self.on_click())


        self.name.raise_()
        self.passw.raise_()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendace Calculator"))
        self.pushButton.setText(_translate("MainWindow", "LOGIN"))
    def perform(self):
        name=self.name.text()
        password=self.passw.text()
        student = self.main(name, password)
        if student is not None:
            attendance_info = student.attendance.get_full_information()
            subject_info,sub_name=student.subjects.all_subject_information()
            if attendance_info['attend'] == 0:
                self.show_result.setText("\tName:"+student.name+"\n\n\tAttendance: {}".format(round(attendance_info['percentage'],2))+"%\n\n\tBunk: {}".format(attendance_info['bunk']))
            else:
                self.show_result.setText("\tName:"+student.name+"\n\n\tAttendance: {}".format(round(attendance_info['percentage'],2))+"%\n\n\tAttend: {}".format(attendance_info['attend']))
    def on_click(self):
        if self.count==False:
            self.count=True
            perform=threading.Thread(target=self.perform)
            perform.start()
            self.show_result.setStyleSheet("background:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383736, stop: 1 #131415);color:white;")
            self.show_result.raise_()
            self.pushButton.setText('Logout')
        else:
            self.count = False
            self.name.setText("")
            self.passw.setText("")
            self.show_result.setText("")
            self.show_result.setStyleSheet("background:transparent;")
            self.name.raise_()
            self.passw.raise_()
            self.pushButton.setText('login')





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
                return self.main(username, password, retry + 1)
            self.show_result.setText('    connected to the server')
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
            except AttributeError:
                self.show_result.setText('    wrong Credentials')
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
