Sun-Top
=======

共享图片链接
django>1.4
1、实现的功能

文件上传
短链接
用户注册
用户登录
登陆后对文件分类查看

2、后端
mysql sqlite

model:
一对多
<1  file_table：
id   filename(CharField)  newname path size type  user(foreign key)
filename = models.ImageField(upload_to=%Y/%m/%d)
newname = models.CharField(max_length=20,unique=True)
path = models.CharField(max_length=10)
size = models.CharField(max_length=10)
type = models.CharField(max_ength=5)
user = models.ForeignKey(User)


<2  user（用django的用户表）：
邮箱  密码

view：
<1、用户管理，包括用户登录、用户注册
<2、文件上传、保存
<3、用户登录查看文件分类输出


template:
<1、注册界面、用户登录界面
<2、首页
<3、用户界面，可以分类查看（排序），搜索
<4、用户settings界面



3、前端
bootstrap
