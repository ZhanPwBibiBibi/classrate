# classrate
本项目主要用于GZHU教务系统的信息抓取。（暂未适配其他学校的教务系统）可用于：

* [x] 了解广州大学选修课预选课时的选课情况，以便全面的了解选课信息，避免选择最热门的课程又不至于选择最冷门的课程。
* [x] 个人信息获取
* [x] 个人成绩获取
* [x] 专业课表获取

## 使用方法
使用非常简单，首先确保你以及正确配置了*Webdriver for Chrome*， 并且Chrome的版本在64以上，Chrome版本太低将不支持*headless mode*，然后就十分简单了：

```python
from spider import Student

if __name__ == '__main__':
    student = Student('your_username', 'your_password')
    student.get_personal_info()
    student.get_class_table()
    student.get_personal_score()
    # 只有当预选课系统开放的时候才有用
    student.get_pre_class_picked()
```

然后，哇，出结果啦～～


### 注意
```python
# requirements.txt:
beautifulsoup4==4.5.3
pygal==2.4.0
selenium==3.4.3
```

PS. 推荐选择热门程度为0.8-1之间的课程，避免人数过少而不开课，或是人数过多被踢导致要参加惨无人道的抢课大战。








