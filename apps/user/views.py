from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegisterSerializer


class UserView(CreateAPIView):
    """
    注册
    """

    serializer_class = RegisterSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = RegisterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsernameIsExistedView(APIView):
    """
    get:
    获取指定用户名数据库已存在个数
    """
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # count = user.count()
        one_dict = {
            'username': username,
            'count': count
        }

        return Response(one_dict)


class EmailIsExistedView(APIView):
    """
    get:
    获取指定邮箱数据库已存在个数
    """

    def get(self, request, email):
        count = User.objects.filter(email=email).count()
        # count = user.count()
        one_dict = {
            'email': email,
            'count': count
        }

        return Response(one_dict)
