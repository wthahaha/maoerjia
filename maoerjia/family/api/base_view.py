# -*- coding:utf-8 -*-

"""
Base类，将增删改查方法重写
"""

from django.conf import settings
from django.core.exceptions import FieldError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from family.utils import GenToken, JsonResponse, StandardResultsSetPagination
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


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

    queryset = ""
    model = None
    serializer_class = ""
    permission_classes = ()
    filter_fields = ()
    search_fields = ()

    token_generator = GenToken()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(
            data=serializer.data["id"],
            message="success",
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def list(self, request, *args, **kwargs):
        """
        current_search_field: 当前正在查询的字段
        """
        queryset = self.model.objects
        if "queryset" in kwargs:
            queryset = kwargs["queryset"]

        query_fields = self.request.query_params.get("qkeys", "_")
        query_value = self.request.query_params.get("qvalue", None)
        page_params = self.request.query_params.get(
            "current", str(settings.PAGINATION_DEFAULT["current"])
        )
        length_params = self.request.query_params.get(
            "length", str(settings.PAGINATION_DEFAULT["length"])
        )
        current_search_field = ""
        try:
            fields = clean_fields(query_fields.split("_"))
            qvalue = query_value
            Qr = None
            for field in fields:
                current_search_field = field
                q = Q(**{"%s__icontains" % field: qvalue})
                if Qr:
                    # |: 或关系， 只要fields中的任意字段能查出qvalue， 就返回数据
                    # &: 与关系， 只有fields中的所有字段都能查出qvalue， 才返回数据
                    Qr = Qr | q
                else:
                    Qr = q
            queryset = queryset.filter(Qr)
        except FieldError:
            # queryset = queryset.none()
            return JsonResponse(
                error="{0}: 该字段不存在, 或该字段不支持查询".format(current_search_field)
            )
        except Exception:
            queryset = queryset
        queryset = queryset.all()
        paginator = StandardResultsSetPagination()
        page_inter_list = paginator.paginate_queryset(queryset, self.request, view=self)
        serializer = self.get_serializer(page_inter_list, many=True)
        pagination_data = paginator.get_paginated_response(
            serializer.data, page_params=page_params, length_params=length_params
        )
        return JsonResponse(data=pagination_data, message="success")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(
            data=serializer.data, message="success", status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        # 默认允许部分更新
        partial = kwargs.pop("partial", True)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return JsonResponse(message="更新成功", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(message="删除成功", status=status.HTTP_200_OK)
