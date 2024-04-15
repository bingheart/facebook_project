# facebook_project

[reptiles](reptiles) 爬虫脚本

[google_plugins](reptiles%2Fgoogle_plugins) 谷歌插件监听网络请求


```
http://127.0.0.1:8000/tool/set_facebook_posts  接收谷歌插件监听网络请求的帖子数据

http://127.0.0.1:8000/tool/set_facebook_queue 设置爬虫队列
设置帖子队列：
{
    "is_post":"True", //是否爬取帖子
    "page":6, //爬取6页面
    "id":"" //facebook用户ID
}
设置获取用户队列：
{
    "is_post":"False", //爬取用户
    "page":6, //爬取6页面
    "id":"" //facebook用户ID
}

http://127.0.0.1:8000/tool/set_facebook_user  接收谷歌插件监听网络请求的用户数据

http://127.0.0.1:8000/tool/login  登入facebook账号加入Redis

POST

{
    "user_name":"", //facebook账号
    "password":"", //facebook密码
    "code":"" // 2FA code 密码
}

``
