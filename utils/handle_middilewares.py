# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse

'''
class DeclineSpidersMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META.get('HTTP_USER_AGENT').startswith('Mozilla/5.0'):
            return JsonResponse({'ret': False, 'msg': '只能运行浏览器请求'})

        return None

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     pass
    #
    # def process_response(self, request, response):
    #     pass
'''


class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Md1view")

    def process_exception(self, request, exception):
        print("md1 process_exception...")


class Md2(MiddlewareMixin):

    def process_request(self,request):
        print("Md2请求")

    def process_response(self,request,response):
        print("Md2返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):

        print("Md2view")

    def process_exception(self, request, exception):  # 只有报错了才会执行exception
        print("md2 process_exception...")
        return HttpResponse("VIEW异常--md2")


