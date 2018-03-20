# ---------------------------
# Author: ZhanPw
# Email: zhanpw97@gmail.com
# License: MIT
# ---------------------------
import json
from math import floor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from terminaltables import AsciiTable
import re
import pygal

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))


class Student():
    """Spider for GZHU FangZheng system"""

    def __init__(self, username, password):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_window_size(1200, 900)
        self.username = username
        self.password = password
        self.login_url = 'http://202.192.18.189/login_gzdx.aspx'
        self.gauge_chart = pygal.Gauge(human_readable=True)  # 初始化图表
        self.gauge_chart.title = '各门课程的选课率'
        self.gauge_chart.range = [0, 3]
        self.__login()

    def __get_current_url(self):
        return list(self.browser.current_url)[20]

    def __login(self):
        self.browser.get(self.login_url)
        user = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        password = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        submit = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fm1 > div.row.btn-row > input.btn-submit"))
        )
        user.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()
        login_state = re.search('.*?class="errors">.*?</div>', self.browser.page_source)
        self.url_last_num = self.__get_current_url()
        self.today_url = '202.192.18.18' + self.url_last_num
        if login_state:
            print('学号或密码错误，请重新输入')
            exit()

    def get_personal_info(self):
        self.browser.get('http://' + self.today_url + '/xsgrxx.aspx?xh=' + self.username + '&gnmkdm=N121501')
        html = self.browser.page_source
        bsobj = BeautifulSoup(html, 'lxml')
        personal_info = bsobj.find('table', {'class': 'formlist'})
        infos_spliter = re.findall('<td.*?>(.*?)</td>', str(personal_info), re.S)
        infos_spliter_attr = re.findall('<span id="lbxsgrxx_.*?>(.*?)：</span>', str(infos_spliter), re.S)
        infos_spliter_index = re.findall('<span id="(?:lbl.*?|xh|xm).*?>(.*?)</span>', str(infos_spliter), re.S)
        # add zmr
        infos_spliter_index.insert(-3, '')
        self.personal_info = dict(zip(infos_spliter_attr, infos_spliter_index))
        return self.personal_info

    def show_personal_info(self):
        try:
            table_data_1 = [
                [i for i in self.personal_info.keys()][0:10],
                [i for i in self.personal_info.values()][0:10]
            ]
            table_data_2 = [
                [i for i in self.personal_info.keys()][10:20],
                [i for i in self.personal_info.values()][10:20]
            ]
            table_data_3 = [
                [i for i in self.personal_info.keys()][20:30],
                [i for i in self.personal_info.values()][20:30]
            ]
            table_data_4 = [
                [i for i in self.personal_info.keys()][30:40],
                [i for i in self.personal_info.values()][30:40]
            ]
            table_data_5 = [
                [i for i in self.personal_info.keys()][40:50],
                [i for i in self.personal_info.values()][40:50]
            ]
            table_data_6 = [
                [i for i in self.personal_info.keys()][50:60],
                [i for i in self.personal_info.values()][50:60]
            ]
            table_1 = AsciiTable(table_data_1)
            table_2 = AsciiTable(table_data_2)
            table_3 = AsciiTable(table_data_3)
            table_4 = AsciiTable(table_data_4)
            table_5 = AsciiTable(table_data_5)
            table_6 = AsciiTable(table_data_6)
            for i in range(1, 7):
                print(eval('table_' + str(i) + '.table'))

        except AttributeError:
            print('## get_personal_info should be run first. ##')

    def score_pdf_generate(self):
        c = Canvas('score_list.pdf', pagesize=A4)
        width, height = A4  # keep for later
        # initialize paper
        c.drawImage('GZHU_title.png', 90, 740, width=13 * cm, height=2.3 * cm, mask=None)
        c.setStrokeColorRGB(1, 0, 0)
        c.line(60, 735, 545, 735)
        c.drawImage('GZHU_seal.png', 410, 75, width=4 * cm, height=3 * cm, mask=None)
        c.setStrokeColorRGB(1, 0, 0)
        c.line(60, 60, 545, 60)

        c.setFont('STSong-Light', 12)
        c.drawString(width / 2 - 1.5 * cm, 720, '学生学业成绩表')

        c.setFont('STSong-Light', 9)
        c.drawString(70, 700, '学号:  ')
        c.drawString(190, 700, '姓名:  ' + self.personal_info['姓名'])
        c.drawString(310, 700, '出生日期:  ')
        c.drawString(450, 700, '学制:  ')
        c.drawString(70, 685, '专业:   ' + self.personal_info['专业名称'])
        c.drawString(310, 685, '在校学习起止年月:  ')
        c.drawString(420, 685, '至')
        c.drawString(485, 700, '年')
        c.drawString(120, 665, '课程名称')
        c.drawString(240, 665, '学分')
        c.drawString(270, 665, '成绩')
        c.drawString(370, 665, '课程名称')
        c.drawString(490, 665, '学分')
        c.drawString(520, 665, '成绩')
        c.drawString(270, 30, '第  1  页/共  1  页')

        c.setFont('Times-Roman', 9)
        c.drawString(95, 700, self.personal_info['学号'])
        c.drawString(350, 700, self.personal_info['出生日期'])
        c.drawString(480, 700, self.personal_info['学制'])
        c.drawString(390, 685, self.personal_info['入学日期'][0:4] + '-' + self.personal_info['入学日期'][4:6])
        c.drawString(430, 685, str(int(self.personal_info['入学日期'][0:4]) + int(self.personal_info['学制'])) + '-' +
                     '07')

        # draw score
        c.setFont('STSong-Light', 8)
        count = 0
        bias = 0
        bias_2 = 0
        current_year = ''
        current_term = ''
        for i in range(1, len(self.score_info) - 1):

            if count < 43:
                if current_year != self.score_info[i][0] or current_term != self.score_info[i][1]:

                    c.setFont('Times-Roman', 8)
                    c.drawString(80, 650 - bias, self.score_info[i][0])
                    c.drawString(145, 650 - bias, self.score_info[i][1])
                    c.setFont('STSong-Light', 8)
                    c.drawString(75, 650 - bias, '(')
                    c.drawString(120, 650 - bias, '学年第')
                    c.drawString(150, 650 - bias, '学期')
                    c.drawString(170, 650 - bias, ')')

                    current_year = self.score_info[i][0]
                    current_term = self.score_info[i][1]
                    bias = bias + 13
                    count = count + 1

                c.setFont('STSong-Light', 8)
                c.drawString(70, 650 - bias, self.score_info[i][3])
                if self.score_info[i][8] in ['优', '良', '中', '差']:
                    c.drawString(275, 650 - bias, self.score_info[i][8])
                else:
                    c.setFont('Times-Roman', 8)
                    c.drawString(275, 650 - bias, self.score_info[i][8])
                c.setFont('Times-Roman', 8)
                c.drawString(243, 650 - bias, self.score_info[i][6])
                bias = bias + 13
                count = count + 1
            else:
                if current_year != self.score_info[i][0] or current_term != self.score_info[i][1]:

                    c.setFont('Times-Roman', 8)
                    c.drawString(330, 650 - bias_2, self.score_info[i][0])
                    c.drawString(395, 650 - bias_2, self.score_info[i][1])
                    c.setFont('STSong-Light', 8)
                    c.drawString(325, 650 - bias_2, '(')
                    c.drawString(370, 650 - bias_2, '学年第')
                    c.drawString(400, 650 - bias_2, '学期')
                    c.drawString(420, 650 - bias_2, ')')

                    current_year = self.score_info[i][0]
                    current_term = self.score_info[i][1]
                    bias_2 = bias_2 + 13
                    count = count + 1

                c.setFont('STSong-Light', 8)
                c.drawString(320, 650 - bias_2, self.score_info[i][3])
                if self.score_info[i][8] in ['优', '良', '中', '差']:
                    c.drawString(525, 650 - bias_2, self.score_info[i][8])
                else:
                    c.setFont('Times-Roman', 8)
                    c.drawString(525, 650 - bias_2, self.score_info[i][8])
                c.setFont('Times-Roman', 8)
                c.drawString(493, 650 - bias_2, self.score_info[i][6])
                bias_2 = bias_2 + 13
                count = count + 1
            c.setFont('STSong-Light', 8)
        if count < 39 :
            ver_bias = bias
            hor_bias = 250
        else:
            ver_bias = bias_2
            hor_bias = 0
        c.drawString(320-hor_bias, 650 - ver_bias, '***************************成绩单总计***************************')
        c.drawString(320-hor_bias, 650 - ver_bias - 39, '****************************以下空白****************************')
        c.drawString(320-hor_bias, 650 - ver_bias - 13, '已获总学分:  ')
        c.drawString(320-hor_bias, 650 - ver_bias - 26, '平均学分绩点（                ）:  ')
        c.setFont('Times-Roman', 8)
        c.drawString(378-hor_bias, 650 - ver_bias - 26, '0.0-5.0')
        c.drawString(370-hor_bias, 650 - ver_bias - 13, self.xuefen)
        c.drawString(420-hor_bias, 650 - ver_bias - 26, self.jidian)

        c.save()
        c.showPage()

    def get_class_table(self):
        self.browser.get('http://' + self.today_url + '/tjkbcx.aspx?xh=' + self.username + '&gnmkdm=N121601')
        html = self.browser.page_source
        bsobj = BeautifulSoup(html, 'lxml')
        self.class_table = bsobj.find('table', {'id': 'Table6'})
        infos_spliter = re.findall('<td.*?>(.*?)</td>', str(self.class_table), re.S)
        index_list = []
        for index, item in enumerate(infos_spliter):
            if item in ['早晨', '第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节']:
                index_list.append(index)

        rep = {'<br/>': '\n', '<font color="red">': '', '</font>': '', '第3节': '第2节', '第5节': '第3节', '第7节': '第4节',
               '第9节': '第5节'}
        for t in range(len(infos_spliter)):
            for i, j in rep.items():
                infos_spliter[t] = infos_spliter[t].replace(i, j)

        class_table_dict = {
            'time': infos_spliter[0:8],
            'morning': infos_spliter[index_list[0]:index_list[1] - 1],
            'first': infos_spliter[index_list[1]:index_list[2] - 1],
            'second': infos_spliter[index_list[3]:index_list[4] - 1],
            'third': infos_spliter[index_list[5]:index_list[6] - 1],
            'forth': infos_spliter[index_list[7]:index_list[8] - 1],
            'fifth': infos_spliter[index_list[9]:index_list[10] - 1]
        }
        self.class_table = class_table_dict

    def show_class_table(self):
        try:
            table_data = [
                [i for i in self.class_table["time"]],
                [i for i in self.class_table["morning"]],
                [i for i in self.class_table["first"]],
                [i for i in self.class_table["second"]],
                [i for i in self.class_table["third"]],
                [i for i in self.class_table["forth"]],
                [i for i in self.class_table["fifth"]]

            ]
            table = AsciiTable(table_data)
            print(table.table)
        except AttributeError:
            print('## get_class_table should be run first. ##')

    def get_personal_score(self):
        self.browser.get('http://' + self.today_url + '/xscj_gc.aspx?xh=' + self.username + '&gnmkdm=N121605')
        ask = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#Button2"))
        )
        ask.click()

        html = self.browser.page_source
        bsobj = BeautifulSoup(html, 'lxml')
        infos = bsobj.tbody.find_all('td')
        grade = []
        for item in infos:
            grade.append(item.get_text())
        score_info = []
        for i in range(0, len(grade), 15):
            if grade[i + 6] in ['0', '1', '2', '3', '4', '5']:
                grade[i + 6] = grade[i + 6] + '.0'
            score_info.append(grade[i:i + 15])
        self.score_info = score_info

        self.jidian = re.findall('平均学分绩点：(.*?)</b>', html, re.S)[0]
        self.xuefen = re.findall('获得学分(.*?)；', html, re.S)[0]
        return self.score_info

    def show_personal_score(self):
        try:
            table_data = self.score_info
            table = AsciiTable(table_data)
            print(table.table)

        except AttributeError:
            print('## get_personal_score should be run first. ##')

    def show_jidian(self):
        try:
            print('绩点: ' + str(self.jidian))
        except AttributeError:
            print('## get_personal_score should be run first. ##')

    def score_to_GPA(self):
        try:
            mult_info = []
            for i in range(1, len(self.score_info)):
                if floor(float(self.score_info[i][7])) == 5:
                    self.score_info[i][7] = 4
                mult_info.append(floor(float(self.score_info[i][7])))
            self.GPA = round(sum(mult_info) / (len(mult_info)), 2)
            print('GPA: ' + str(self.GPA))
        except AttributeError:
            print('## get_personal_score should be run first. ##')

    def get_pre_class_picked(self):
        self.browser.get('http://' + self.today_url + '/xf_xsqxxxk.aspx?xh=' + self.username)
        item_num = WebDriverWait(self.browser, 1000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dpkcmcGrid_txtPageSize")))
        item_num.clear()
        html = self.browser.page_source
        try:
            for page in range(1, 14):
                for item in self.__parse_page(html):
                    print(item)
                html = self.__next_page()
        except TimeoutException:
            self.gauge_chart.render_in_browser()

    def __parse_page(self, html):
        class_infos_pattern = re.compile("<tr(.*?)</tr>", re.S)
        class_infos = re.findall(class_infos_pattern, html)
        try:
            for class_info in class_infos:
                if "第" or "教务处 " in class_info:
                    a_class_info = {
                        "class_name": re.findall(
                            "kcxx','.*?resizable=0,width=540,height=450,left=120,top=60'" + '\)">' + "(.*?)</a></td>",
                            class_info, re.S),
                        "teacher_name": re.findall(
                            "jsxx','.*?resizable=0,width=540,height=450,left=120,top=60'" + '\)">' + "(.*?)</a></td>",
                            class_info, re.S),
                        "all": re.findall("</td><td>([0-9]+)</td><td>-?[0-9]+</td><td>", class_info, re.S),
                        "rest": re.findall("</td><td>[0-9]+</td><td>(-?[0-9]+)</td><td>", class_info, re.S)
                    }
                if a_class_info["class_name"]:
                    self.__save_to_file(a_class_info)
                    yield a_class_info
                    rate = (int(a_class_info["all"][0]) - int(a_class_info["rest"][0])) / int(a_class_info["all"][0])
                    self.gauge_chart.add(str(a_class_info["class_name"]) + '---' + str(a_class_info["teacher_name"]),
                                         rate)
        except TimeoutException:
            print("课程信息获取完成")

    def __save_to_file(self, content):
        print('正在写入文本文件...')
        with open('class_info.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content, ensure_ascii=False) + '\n')
            f.close()

    def __next_page(self):
        next = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#dpkcmcGrid_btnNextPage")))
        next.click()
        html = self.browser.page_source
        return html

    def exit(self):
        self.browser.quit()
        exit()
