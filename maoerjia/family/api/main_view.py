"""
Author: wangteng
定义视图函数
"""
from django.conf import settings
from rest_framework import permissions
from family.models import HomeBasicInfo
from family.serializers import HomeBasicInfoSerializer, PetInfo
from .base_view import CustomViewBase


class HomeBasicInfoView(CustomViewBase):
    """
    家庭基本信息视图
    """

    model = HomeBasicInfo  # 要序列化的model，必须
    queryset = model.objects.all() # 根据model查询出的queryset， 必须
    serializer_class = HomeBasicInfoSerializer # 序列化器， 必须
    permission_classes = (permissions.AllowAny,) # 权限控制， 必须


class PetInfoView(CustomViewBase):
    pass