
import logging,json,os
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions,mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import Reports
from .serializers import ReportsModelSerializer
from django.conf import settings
from django.http.response import StreamingHttpResponse
from .utils import get_file_content
from django.utils.encoding import escape_uri_path

logger = logging.getLogger('mytest')
class ReportsViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer
    # pagination_class = MyPagination
    def  list(self, request, *args, **kwargs):
        response=super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            if item['result']=='1':
                item['result'] = 'Pass'
            elif item['result']=='0':
                item['result'] = 'Fail'
            # item.pop('html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        results = response.data
        results['summary']=json.loads(results['summary'])
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        instance=self.get_object()
        html=instance.html
        name=instance.name
        # 获取测试报告的输出路径
        reports_dir=settings.REPORTS_DIR
        # 拼接测试报告路径及文件名
        reports_full_dir=os.path.join(reports_dir,f"{name}.html")

        #生成html文件。存放在reports目录下。如果已存在，则不再重复生成
        if not os.path.exists(reports_full_dir):
            with open(reports_full_dir,"w",encoding="utf-8") as file:
                file.write(html)

        response = StreamingHttpResponse(get_file_content(reports_full_dir))
        html_file_name=escape_uri_path(name+'.html')

        response["Content-Type"]='application/octet-stream'
        response["Content-Disposition"]=f"attachment; filename*=UTF-8''{html_file_name}"
        return response



