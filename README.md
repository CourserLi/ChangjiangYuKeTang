# ChangjiangYuKeTang
长江雨课堂自动签到脚本

### 运行说明
每天上午开始 10 点开始执行，直到晚上 16 点关闭

每半个小时检查一次，共检查 12 次

### 代码说明
1. 你只需要填写 `PHONE` 和 `PASSWORD`（在代码里面），也就是长江雨课堂的手机账号和密码，如果没注册的话，在长江雨课堂的 “账号绑定” 里面设置就好了 ~
2. 你还需要填写 `TJ_ACCOUNT` 和 `TJ_PASSWORD`（在代码里面），是验证码识别网站的账号和密码，同样也是注册即可，建议再往里面充 10 块钱，应该可以用一学期 ~

PS：其他的懒得说明，直接看代码就好

### 运行环境
**前置条件**
1. chromedriver.exe 放在和 python.exe 同目录
2. 下载 python 必要库 `pip install -r requirements.txt`

**运行方式**

我是放在 Windows 服务器中运行的，下载了 python 并配置好环境

定时运行：控制面板 -> 系统和安全 -> 管理工具 -> 计划任务 -> 创建基本任务 -> 脚本选择 -> `C:\Users\Administrator\Desktop\ChangjiangYuKeTang\run.bat`

其中 run.bat 的内容为 `C:\Users\Administrator\AppData\Local\Programs\Python\Python310\python.exe C:\Users\Administrator\Desktop\ChangjiangYuKeTang\yuketang.py`
