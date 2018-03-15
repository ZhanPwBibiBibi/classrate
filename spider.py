import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import pygal
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome()

browser.set_window_size(1200, 900)

gauge_chart = pygal.Gauge(human_readable=True)  # 初始化图表
gauge_chart.title = '各门课程的选课率'
gauge_chart.range = [0, 3]

my_username = None
my_password = None


def login():
    while True:
        global my_username
        global my_password
        my_username = input('请输入学号: ')
        my_password = input('请输入密码: ')

        print('正在登陆...')
        browser.get('https://cas.gzhu.edu.cn/cas_server/login')
        user = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        password = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        submit = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fm1 > div.row.btn-row > input.btn-submit"))
        )
        user.send_keys(my_username)
        password.send_keys(my_password)
        submit.click()
        login_state = re.search('.*?class="errors">.*?</div>', browser.page_source)
        if login_state:
            print('学号或密码错误，请重新输入')
        else:
            break


def to_pri_info(my_username):
    print('正在跳转个人信息页面...')
    browser.get('http://202.192.18.183/xsgrxx.aspx?xh=' + my_username + '&gnmkdm=N121501')
    html = browser.page_source
    print('正在采集')
    pri_info = {
        "id": re.findall('<td><span id="xh">(.*?)</span></td>', html, re.S),
        "photo": re.findall('<td rowspan="6"><img id="xszp" src="(.*?)" alt="照片" align="AbsMiddle"', html, re.S),
        "name": re.findall('<td><span id="xm">(.*?)</span></td>', html, re.S),
        "sex": re.findall('<td><span id="lbl_xb">(.*?)</span></td>', html, re.S),
        "enro_date": re.findall('<td colspan="2"><span id="lbl_rxrq">(.*?)</span></td>', html, re.S),
        "bir_date": re.findall('<td><span id="lbl_csrq">(.*?)</span></td>', html, re.S),
        "mid_school": re.findall('<td colspan="2"><span id="lbl_byzx">(.*?)</span></td>', html, re.S),
        "nation": re.findall('<td><span id="lbl_mz">(.*?)</span></td>', html, re.S),
        "ori_from": re.findall('</span><span id="lbl_jg">(.*?)</span></td>', html, re.S),
        "pol_sta": re.findall('<span id="lbl_zzmm">(.*?)</span></td>', html, re.S),
        "phone": re.findall('<span id="lbl_lxdh">(.*?)</span></td>', html, re.S),
        "gra_place": re.findall('<span id="lbl_lys">(.*?)</span></td>', html, re.S),
        "exm_num": re.findall('<span id="lbl_zkzh">(.*?)</span></td>', html, re.S),
        "birth_palce": re.findall('<span id="lbl_csd">(.*?)</span></td>', html, re.S),
        "id_number": re.findall('<span id="lbl_sfzh">(.*?)</span></td>', html, re.S),
        "edu_sta": re.findall('<span id="lbl_CC">(.*?)</span></td>', html, re.S),
        "department": re.findall('<span id="lbl_xy">(.*?)</span></td>', html, re.S),
        "home_place": re.findall('<span id="lbl_jtszd">(.*?)</span></td>', html, re.S),
        "major": re.findall('<span id="lbl_zymc">(.*?)</span></td>', html, re.S),
        "class": re.findall('<span id="lbl_xzb">(.*?)</span></td>', html, re.S),
        "english_grade": re.findall('<span id="lbl_YYCJ">(.*?)</span></td>', html, re.S),
        "study_year": re.findall('<span id="lbl_xz">(.*?)</span></td>', html, re.S),
        "stu_proof": re.findall('<span id="lbl_xjzt">(.*?)</span></td>', html, re.S),
        "grade": re.findall('<span id="lbl_dqszj">(.*?)</span></td>', html, re.S),
        "stu_exm_num": re.findall('<span id="lbl_ksh">(.*?)</span></td>', html, re.S)
    }
    print(pri_info)


def to_jiaowu(my_username):
    print('正在跳转选课系统...')
    browser.get('http://202.192.18.185/xf_xsqxxxk.aspx?xh=' + my_username)
    item_num = WebDriverWait(browser, 1000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#dpkcmcGrid_txtPageSize"))
    )
    item_num.clear()
    html = browser.page_source
    return html


def parse_page(html):
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
                    save_to_file(a_class_info)
                    yield a_class_info
                    rate = (int(a_class_info["all"][0]) - int(a_class_info["rest"][0])) / int(a_class_info["all"][0])
                    gauge_chart.add(str(a_class_info["class_name"]) + '---' + str(a_class_info["teacher_name"]), rate)
    except TimeoutException:
        print("课程信息获取完成")


def next_page():
    print('正在翻页...')
    next = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#dpkcmcGrid_btnNextPage"))
    )
    next.click()
    html = browser.page_source
    return html


def save_to_file(content):
    print('正在写入文本文件...')
    with open('class_info.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main():
    login()
    # print(to_pri_info(my_username))

    html = to_jiaowu(my_username)
    try:
        for page in range(1, 14):
            for item in parse_page(html):
                print(item)
            html = next_page()
    except TimeoutException:
        print("课程信息获取完成")
        gauge_chart.render_in_browser()


if __name__ == '__main__':
    main()

# zhanpw
