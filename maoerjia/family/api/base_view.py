# -*- coding:utf-8 -*-

"""
Base类，将增删改查方法重写
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.utils import JsonResponse, StandardResultsSetPagination, GenToken


class CustomViewBase(viewsets.ModelViewSet):
    """
    自定义视图基类
    方法介绍：
    list: 列出所有数据， 对应http方法为get
    retrieve: 列出指定数据， 对应http方法为get
    create: 新增数据， 对应http方法为post
    update: 更新数据， 对应http方法为put
    destroy: 删除数据， 对应http方法为delete
    """

    queryset = ''
    serializer_class = ''
    permission_classes = ()
    filter_fields = ()
    search_fields = ()
    # pagination_class = customPagination
    # filter_class = customFilter
    # filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    token_generator = GenToken()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data['id'], message="success", status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # 如果返回的数据需要分页， 需要使用分页器、从请求中获取页码和每页数据量
        page_params = self.request.query_params.get(
            "page", str(settings.PAGINATION_DEFAULT["page"]))
        length_params = self.request.query_params.get(
            "length", str(settings.PAGINATION_DEFAULT["length"]))

        paginator = StandardResultsSetPagination()
        queryset = self.filter_queryset(self.get_queryset())

        page_inter_list = paginator.paginate_queryset(
            queryset, self.request, view=self)
        serializer = self.get_serializer(page_inter_list, many=True)
        pagination_data = paginator.get_paginated_response(
            serializer.data, page_params=page_params, length_params=length_params)
        return JsonResponse(data=pagination_data, message="success")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, message="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # 默认允许部分更新
        partial = kwargs.pop('partial', True)

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return JsonResponse(message="更新成功", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(message="删除成功", status=status.HTTP_200_OK)
