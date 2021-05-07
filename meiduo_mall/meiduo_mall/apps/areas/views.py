from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializaes import AreaSerializer, SubAreaSerializer

'''
# 方式一
class AreaProvinceView(ListCacheResponseMixin, ListAPIView):
    queryset = Area.objects.filter(parent=None)  # 没有父类说明都是省级，不添加条件会查询所有的区域
    serializer_class = AreaSerializer
    pagination_class = None # 屏蔽分页，下拉选择地址时不需要分页


class SubAreaView(RetrieveCacheResponseMixin, RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = SubAreaSerializer
'''


# 方式二
class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    # 禁用分页功能
    pagination_class = None

    def get_serializer_class(self):
        '''提供序列化器'''
        if self.action == 'list':  # 查询列表
            return AreaSerializer
        else:
            return SubAreaSerializer

    def get_queryset(self):
        '''提供数据集'''
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()
