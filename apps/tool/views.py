import json
import re

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from tool.analysis import FacebookAnalysis
from tool.models import Posts


# Create your views here.
@api_view(['POST'])
def set_facebook_posts(request):
    for json_data in str(request.data['data']).split("\n"):
        json_data = json.loads(json_data)
        if json_data.get('label'):
            if json_data.get('data'):
                data = json_data['data']
                if data.get('node'):
                    FacebookAnalysis.get_posts(data)
        else:
            data=json_data.get('data')
            if data:
                viewer=data.get('viewer')
                if viewer:
                    news_feed=viewer.get('news_feed')
                    if news_feed:
                        edges=news_feed.get('edges')
                        for edge in edges:
                            FacebookAnalysis.get_posts(edge)
    return HttpResponse(json.dumps({"data": {}}), "application/json")

@api_view(['POST'])
def set_facebook_queue(request):
    is_post = request.data.get('is_post',False)
    page = request.data.get('page',1)
    id = request.data.get('id',None)
    if id == None:
        return HttpResponse(json.dumps({"data": {'message': "ID 不能为空"}}), "application/json")
    #获取爬取的用户资料
    redis_conn = get_redis_connection("default")
    redis_conn.rpush("crawler_queue", json.dumps({'is_post':is_post,'page':page,'id':id}))
    return HttpResponse(json.dumps({"data": {'message': "加入队列成功"}}), "application/json")
@api_view(['POST'])
def set_facebook_user(request):
    FacebookAnalysis.set_uaers(json.loads(request.data['data'])['data'])
    return HttpResponse(json.dumps({"data": {'message': "保存成功"}}), "application/json")

@api_view(['POST'])
def login(request):
    user_name = request.data.get('user_name',None)
    password = request.data.get('password',None)
    code = request.data.get('code',None)
    if user_name == None or password == None or code == None:
        return HttpResponse(json.dumps({"data": {'message': '請輸入帳號、密碼、驗證碼'}}), "application/json")
    else:
        # 连接到Redis
        redis_conn = get_redis_connection("default")
        # 将JSON数据推送到Redis队列中
        request.data['is_login'] = False
        redis_conn.rpush("user_queue", json.dumps(request.data))
        return HttpResponse(json.dumps({"data": {'message':"加入队列成功"}}), "application/json")




@api_view(['POST'])
def post_facebook_secret(request):
    return HttpResponse(json.dumps({"data": {}}), "application/json")

@api_view(['GET'])
def get_posts(request):
    posts=Posts.objects.all()
    list_posts=[]
    for data in posts:
        list_posts.append(data.get_map())
    return HttpResponse(json.dumps({"data": {'list_posts':list_posts}}), "application/json")


@api_view(['POST'])
def get_account(request):
    pass



@api_view(['POST'])
def crawler_queue(request):
    #获取爬虫队列
    pass

@api_view(['POST'])
def post_list(request):
    #获取帖子列表
    pass

