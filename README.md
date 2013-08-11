Sun-Top
=======
#网站介绍
- 网站首页
![](http://luyadong.smugmug.com/aaa/i-dp6Kqmf/0/XL/x-XL.png)

- upload界面
![](http://luyadong.smugmug.com/Suntop/i-gk889sF/0/XL/upload-XL.png)

- 注册界面
![](http://luyadong.smugmug.com/Suntop/i-pfSCmkB/0/XL/registe-XL.png)

- 登录界面
![](http://luyadong.smugmug.com/Suntop/i-2FNNjkw/0/XL/login-XL.png)

- 所有用户共享图片
![](http://luyadong.smugmug.com/Suntop/i-tGB58v8/0/XL/share-XL.png)

- 当前用户共享图片
![](http://luyadong.smugmug.com/Suntop/i-c2sjLg2/0/XL/my_share-XL.png)

#网站框架
- 前端  
用到bootstrap

- 后端  
Django==1.4.5  
MySQL-python==1.2.4  
Wand==0.3.3  
gunicorn==17.5  
python-memcached==1.53  

- 数据库  
线下用sqlite测试，线上可以用mysql


#环境搭建  
 #yum install setuptool  
 #easy_install virtualenv  
 #virtualenv --no-site-package Suntop  
 #cd Suntop  
 #git init .  
 #git clone https://github.com/luyadong/Sun-Top.git  
 #sourice bin/active  
 #cd Sun-Top  
 #pip install -r pip-req.txt  
 #python manage.py syncdb  
 #python manage.py runserver IP:PORT
