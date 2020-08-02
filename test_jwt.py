# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/7/22 20:55 
  @Auth : 可优
  @File : test_jwt.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import jwt

# 第一部分的header，一般不需要指定，有默认值

# 第二部分，可以指定后端需要存放的一些非敏感的信息
payload = {
    'username': '小李',
    'age': 18
}
# 服务端创建token令牌的过程
token = jwt.encode(payload, key='666')

# 服务端对前端用户传递的token进行解密过程
one_var = jwt.decode(token, key='667')
pass

