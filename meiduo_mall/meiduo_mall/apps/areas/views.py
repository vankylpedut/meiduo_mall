from django.shortcuts import render
from rest_framework import mixins
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer
from users.models import Address
from users.serializers import UserAddressSerializer, AddressTitleSerializer

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


class AddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    '''用户地址管理
    1、用户地址的增删改查处理
    2、设置默认地址：put
    3、设置地址标题：put
    '''

    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    # query_set = Address.object.all()  # 会返回所有用户的地址，没有限定成登陆用户的地址
    # queryset = Address.objects.filter(user=self.request.user,is_deleted=False)  # 这里不能用该方式查询是因为数据库不识别self

    def get_queryset(self):
        #  获取当前登录用户的地址
        # return Address.object.filter(user=self.request.user,is_deleted=False) # 条件筛选出登录用户的地址
        return self.request.user.addresses.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        count = request.user.addresses.count()
        if count >= 3:  # 每个用户最多不能超过3个地址
            return Response({'message': '地址个数已达上限'}, status=400)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        '''用户地址列表数据'''
        queryset = self.get_queryset()  # 获取登陆用户的所有地址
        serializer = self.get_serializer(queryset, many=True)  # 获取serializer.data列表
        return Response({
            'user_id': request.user.id,
            'default_address_id': request.user.default_address_id,
            'limit': 3,
            'addresses': serializer.data,
        })

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        '''删除地址'''
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response({'message': '删除成功'}, status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        '''设置默认地址'''
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        '''修改标题'''
        address = self.get_object()
        serializer = AddressTitleSerializer()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
