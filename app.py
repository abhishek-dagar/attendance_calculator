import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
import threading
from flask import Flask, render_template, request, session,redirect

from Student import Student

import os
...
port = int(os.environ.get('PORT', 5000))
#########################################################
class Scrape(object):
    def __init__(self):
        self.urls = []
        self.dataset = []

    def newUrl(self, url):
        t1 = threading.Thread(target=scapAttendance,args=())


def scapAttendance(s, headers, attendance_url):
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


def main(username, password, retry=0):
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
            return main(username, password, retry + 1)
        print('connected to the server')
        soup = BeautifulSoup(r.text, 'html5lib')
        login_data['_token'] = soup.find(
            'input', attrs={'name': '_token'})['value']
        r = s.post(form_action_url, data=login_data, headers=headers)

        # To extract student name from the dashboard page
        page = "".join(line.strip() for line in r.text.split("\n"))
        soup = BeautifulSoup(page, 'html5lib')
        try:
            student_data.name = soup.find(class_="user-panel").find('p').text
            print('logged in')
        except AttributeError:
            print('wrong Credentials')
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
app= Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict",methods=['POST'])
def predict():
    features = [value for value in request.form.values()]
    username = features[0]
    password = features[1]
    student = main(username, password)
    if student is not None:
        print('\n')
        attendance_info = student.attendance.get_full_information()
        student_name=student.name
        percent="Percentage: {}".format(attendance_info['percentage'])
        bunk_or_attend=""
        if attendance_info['attend'] == 0:
            bunk_or_attend="Bunk: {}".format(attendance_info['bunk'])
        else:
            bunk_or_attend="Attend: {}".format(attendance_info['attend'])
    return render_template("index.html",stud_name=student_name,b_o_a=bunk_or_attend,percent=percent)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
    '''while True:
        print('******************************')
        username = input('username: ')
        password = input('password: ')
        student = main(username, password)
        if student is not None:
            print('\n')
            attendance_info = student.attendance.get_full_information()
            print(student.name)
            print("Percentage: {}".format(attendance_info['percentage']))
            if attendance_info['attend'] == 0:
                print("Bunk: {}".format(attendance_info['bunk']))
            else:
                print("Attend: {}".format(attendance_info['attend']))

        print('******************************')
        print('\n\n')'''

    # master = tk.Tk()
    # tk.Label(master, text="First Name").grid(row=0)
    # tk.Label(master, text="Last Name").grid(row=1)
    #
    # username_input = tk.Entry(master)
    # password_input = tk.Entry(master)
    # username_input.grid(row=0, column=1)
    # password_input.grid(row=1, column=1)
    #
    #
    # def get_username():
    #     return username_input.get()
    #
    #
    # def get_password():
    #     return password_input.get()
    #
    #
    # def attendance_info_window():
    #     student_data = main(get_username(), get_password())
    #     window = tk.Toplevel(master)
    #     attendance_info = student_data.attendance.get_full_information()
    #     tk.Label(window, text=str(student_data.name)).grid(row=0)
    #     tk.Label(window, text=attendance_info['percentage']).grid(row=1)
    #     if attendance_info['attend'] == 0:
    #         tk.Label(window, text='Bunk:').grid(row=2)
    #         tk.Label(window, text=str(attendance_info['bunk'])).grid(row=2,column=1)
    #     else:
    #         tk.Label(window, text='attend:').grid(row=2)
    #         tk.Label(window, text=str(attendance_info['attend'])).grid(row=2,column=1)
    #
    #
    # tk.Button(master, command=attendance_info_window, compound="right",
    #           text='Show').grid(row=3,
    #                             column=1,
    #                             )
    #
    # master.mainloop()
