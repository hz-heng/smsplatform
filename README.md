# smsplatform

### 说明：
* 短信发送使用阿里大于的短信api
* 由于阿里大于官方api是Python2版本的，所以这里使用的api是:https://github.com/raptorz/alidayu
### 部署：
1. 在config.py里配置自己申请的阿里大于的APPKEY和SECRET
2. 安装程序依赖：pip install -r requirements.txt
3. 数据库部署
> python manage.py db init  # 初始化迁移脚本  
> python manage.py db migrate  # 执行迁移  
> python manage.py db upgrade  # 更新  
> python manage.py initdata # 初始化管理员账号（用户名：admin 密码：admin） 
### 运行
* 执行python run.py启动程序  
* 浏览器访问http://127.0.0.1:5000
### 截图
![login](https://github.com/hz-heng/smsplatform/blob/master/Screenshots/login.png)
![big](https://github.com/hz-heng/smsplatform/blob/master/Screenshots/big.png)
![small](https://github.com/hz-heng/smsplatform/blob/master/Screenshots/small.png)
