#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-05,22:52"
import re

from django.conf import settings
from django.shortcuts import redirect

class MiddlewareMixin(object):  #写中间件必须继承这个类
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class LoginMiddle(MiddlewareMixin):
    def process_request(self,request):
        '''
        获取当前路径，与白名单匹配
        获取session中的username,不存在则返回登录
        :param request:
        :return:
        '''

        current_url = request.path_info

        for url in settings.VALID_URL:
            regex = "^{0}$".format(url)
            if re.match(regex,current_url):
                return None

        if request.session.get("username"):
            return None
        else:
            return redirect("/login/")