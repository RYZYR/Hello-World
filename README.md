### README

下载需要的包
> 可能有部分缺失，记得之前有个.wheel文件是从一个[网站](https://www.lfd.uci.edu/~gohlke/pythonlibs/)上下载的，然后再本地安装包的,不是直接 pip install的，但当时好像
> 是解决一个什么字符显示还是图形显示的问题的。
> 人脸识别的程序需要的包也不全，还有一些

```
pip install -r requirements.txt
```

数据库使用的是mysql, 数据库的配置信息在工程目录下(srtpProj)的settings.py中。

---

---



### Plan

#### SiteUrlConf

###### ../index/		

**两部分**

 1. **新建课堂部分**： 

    ​	表单 post （设置课程名、第几周、第几节课） [填充Course表]	--->(后台识别程序	开始运行)

 2. **查看以往信息部分**： 	

    ​	表单post（ 选取 哪个班、课程名,第几周和第几节课）[由表单信息获取Course的**主键ID**，再有ID来获取Status表中 **该节课的所有学生状态**]

###### ../newDetail/

	1. 显示课程信息
	1. 显示调用的树莓派摄像头
	1. 下课按钮---->(识别程序结束调用，并将获取的 json数据写入 Status表中) [跳转到index页面]

###### ../inforDetail/ 	   

  	 1. 显示  <>课程<>周<>节  每个学生的数据[(专心数),(签到否)]



------



#### Models

##### 		Class表

​			**字段：班级(pk)**	

​			类型	string

​			*e.g.   一班*

##### 		Student表

​			**字段： 学号(pk)  班级(fk: Class.班级)  姓名**  

​			类型	 int				string		 			string

​			*e.g.		2019xx			一班		*

##### 		Section表	

​			**字段:   ID(pk) 课程名(fk:Course:)   	周数  周几  节数**		

​			类型	int		string		 int	      	 int

​			*e.g.	  12		"高数"  		1		    	2*

##### 		Status表		（由json数据填充）

​			**字段:   ID(pk)   学号(fk: Student.学号)  CourseID(fk: Course.ID)   专心数	签到    签到时间**

​			类型	int			int										int										int		bool       

​			 *e,g.	1				2019xx	  					      12								 	   50           True        2022-3*

​					  *2  				2018xx							 	 12										33			True    2022-3*

**Course表**

​			ID 课程名

​			



----

##### note

1. Django文档中出现的Choice二元组label标签是_("字符串")： _()是 gettext()函数的别名



---

##### Learning

 	1. bootstrap
 	2. ajax



---

Django 相应URL流程:
		以polls应用为例:

​		首页:  index	--对应的url样式--   URLpatterns: 	 **path**('', **views**.**IndexView**.**as_view**(), name='index'),



​		视图相应函数为  indexView类的as_view()函数（具体django文档中基于类的视图）			

​			**views.indexView.as_view()**

​			``

​	点击问题链接





