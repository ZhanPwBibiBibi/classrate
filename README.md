# classrate
本项目主要用于广州大学GZHU教务系统的信息抓取。（暂未适配其他学校的教务系统，如有机会会逐渐适配）可用于： 

* [x] 在预选课阶段获取全校预选课信息
* [x] 个人信息获取
* [x] 个人成绩获取
* [x] 专业课表获取
* [x] 个人信息Pretty Print
* [x] 个人成绩Pretty Print
* [x] 专业课表Pretty Print
* [x] 将5分制绩点换算为4分制GPA



<!-- more -->



## What you need
* 本项目在 Python 3.6 下通过测试, 其他版本未测试。

* 首先确保你以及正确配置了*Webdriver for Chrome*，如果未安装，点[这里](https://docs.seleniumhq.org/projects/webdriver/)了解更多。 

* 并且Chrome的版本在64以上，Chrome版本太低将不支持*headless mode*。

* 然后确保你已经正确安装了如下版本的包：

    ```
    # requirements.txt:
    beautifulsoup4==4.5.3
    pygal==2.4.0
    selenium==3.4.3
    ```

然后，下一步就可以开始使用啦！

```bash
# 在终端下使用将会有更加格式化的输出
# in the terminal will have a more formatted output
from spider import Student

# 初始化
# initialize
student = Student('username', 'password')


student.get_personal_info() # 获取个人信息 Get personal information
student.show_personal_info() # 以表格方式显示个人信息 Pretty print personal information in ASCII table

student.get_class_table() # 获取专业课表 Get class table
student.show_class_table() # 以表格方式显示专业课标 Pretty print class table in ASCII table


student.get_personal_score() # 获取个人成绩 Get personal score
student.show_personal_score() # 以表格方式显示个人成绩 Pretty print personal score in ASCII table

student.show_jidian() # 获取绩点 Show 5-point GPA(jidian)
student.score_to_GPA() # 将分数转换为GPA Convert 5-point GPA(jidian) to 4-point GPA

# 获取全校预选课情况，只有当预选课系统开放的时候才有用 
# Get pre-selection infos.
# Only can be used when the pre-selection system is open.
student.get_pre_class_picked() 


# Don't forget this
student.exit()
    
```


## License
MIT









