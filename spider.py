# ---------------------------
# Author: ZhanPw
# Email: zhanpw97@gmail.com
# License: MIT
# ---------------------------
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import pygal
from selenium.webdriver.chrome.options import Options


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
        print('正在登陆...')
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
        print('正在跳转个人信息页面...')
        self.personal_info = {}
        self.browser.get('http://' + self.today_url + '/xsgrxx.aspx?xh=' + self.username + '&gnmkdm=N121501')
        html = self.browser.page_source
        self.personal_info["student_number"] = re.findall('<td><span id="xh">(.*?)</span></td>', html, re.S),
        self.personal_info["photo"] = re.findall(
            '<td rowspan="6"><img id="xszp" src="(.*?)" alt="照片" align="AbsMiddle"', html,
            re.S),
        self.personal_info["name"] = re.findall('<td><span id="xm">(.*?)</span></td>', html, re.S),
        self.personal_info["sex"] = re.findall('<td><span id="lbl_xb">(.*?)</span></td>', html, re.S),
        self.personal_info["enrollment_date"] = re.findall('<td colspan="2"><span id="lbl_rxrq">(.*?)</span></td>',
                                                           html, re.S),
        self.personal_info["birth_date"] = re.findall('<td><span id="lbl_csrq">(.*?)</span></td>', html, re.S),
        self.personal_info["middle_school"] = re.findall('<td colspan="2"><span id="lbl_byzx">(.*?)</span></td>',
                                                         html, re.S),
        self.personal_info["nation"] = re.findall('<td><span id="lbl_mz">(.*?)</span></td>', html, re.S),
        self.personal_info["origin"] = re.findall('</span><span id="lbl_jg">(.*?)</span></td>', html, re.S),
        self.personal_info["political_status"] = re.findall('<span id="lbl_zzmm">(.*?)</span></td>', html, re.S),
        self.personal_info["phone"] = re.findall('<span id="lbl_lxdh">(.*?)</span></td>', html, re.S),
        self.personal_info["source_area"] = re.findall('<span id="lbl_lys">(.*?)</span></td>', html, re.S),
        self.personal_info["exam_number"] = re.findall('<span id="lbl_zkzh">(.*?)</span></td>', html, re.S),
        self.personal_info["birth_palce"] = re.findall('<span id="lbl_csd">(.*?)</span></td>', html, re.S),
        self.personal_info["id_number"] = re.findall('<span id="lbl_sfzh">(.*?)</span></td>', html, re.S),
        self.personal_info["academic_level"] = re.findall('<span id="lbl_CC">(.*?)</span></td>', html, re.S),
        self.personal_info["institute"] = re.findall('<span id="lbl_xy">(.*?)</span></td>', html, re.S),
        self.personal_info["home_place"] = re.findall('<span id="lbl_jtszd">(.*?)</span></td>', html, re.S),
        self.personal_info["major"] = re.findall('<span id="lbl_zymc">(.*?)</span></td>', html, re.S),
        self.personal_info["class"] = re.findall('<span id="lbl_xzb">(.*?)</span></td>', html, re.S),
        self.personal_info["english_score"] = re.findall('<span id="lbl_YYCJ">(.*?)</span></td>', html, re.S),
        self.personal_info["study_year"] = re.findall('<span id="lbl_xz">(.*?)</span></td>', html, re.S),
        self.personal_info["student_status"] = re.findall('<span id="lbl_xjzt">(.*?)</span></td>', html, re.S),
        self.personal_info["grade"] = re.findall('<span id="lbl_dqszj">(.*?)</span></td>', html, re.S),
        self.personal_info["candidate_number"] = re.findall('<span id="lbl_ksh">(.*?)</span></td>', html, re.S)

        for key, item in self.personal_info.items():
            print(key + ': ' + str(item[0]))
        return self.personal_info

    def get_class_table(self):
        print('正在跳转专业课表...')
        self.browser.get('http://' + self.today_url + '/tjkbcx.aspx?xh=' + self.username + '&gnmkdm=N121601')
        print('正在采集')
        html = self.browser.page_source
        bsobj = BeautifulSoup(html, 'lxml')
        infos = bsobj.find_all('table', {'id': 'Table6'})
        for info in infos:
            class_table = info.get_text()
            # print(info.get_text())
        self.class_table = class_table.replace('\xa0', ' , ')
        print(self.class_table)
        return self.class_table

    def get_personal_score(self):

        print('正在跳转成绩表...')
        self.browser.get('http://' + self.today_url + '/xscj_gc.aspx?xh=' + self.username + '&gnmkdm=N121605')
        print('正在采集')
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
            score_info.append(grade[i:i + 15])
            print(grade[i:i + 15])
        self.score_info = score_info
        return self.score_info

    def get_pre_class_picked(self):
        print('正在跳转选课系统...')
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
            print("课程信息获取完成")
            self.gauge_chart.render_in_browser()

    def __parse_page(self, html):
        print('正在采集...')
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
        print('正在翻页...')
        next = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#dpkcmcGrid_btnNextPage")))
        next.click()
        html = self.browser.page_source
        return html
