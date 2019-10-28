"""
Author: wangteng, qinyu
定义视图函数
"""
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from apps.core.utils import StandardResultsSetPagination
from apps.core.utils import json_response, JsonResponse
from family.models import HomeBasicInfo
from family.serializers import HomeBasicInfoSerializer
from .base_view import CustomViewBase


class HomeBasicInfoView(CustomViewBase):
    """
    家庭基本信息视图
    """

    queryset = HomeBasicInfo.objects.all()
    serializer_class = HomeBasicInfoSerializer

    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        # 如果返回的数据需要分页， 需要使用分页器、从请求中获取页码和每页数据量
        paginator = StandardResultsSetPagination()

        search_params = self.request.query_params.get("search", "")
        page_params = self.request.query_params.get(
            "page", str(settings.PAGINATION_DEFAULT["page"]))
        length_params = self.request.query_params.get(
            "length", str(settings.PAGINATION_DEFAULT["length"]))

        # 根据查询关键字模糊查询
        queryset = Secureykey.objects.filter(
            username__contains=search_params).order_by('createdAt')

        page_inter_list = paginator.paginate_queryset(
            queryset, self.request, view=self)
        serializer_class = SecureykeySerializer(page_inter_list, many=True)
        response = paginator.get_paginated_response(serializer_class.data,\
                    page_params=page_params, length_params=length_params)
        return JsonResponse(data=response, message="success")


class TeamView(CustomViewBase):
    """
    团队认证视图
    """
    queryset = Team.objects.all().order_by('createdAt')
    serializer_class = TeamSerializer
    permission_classes = (permissions.AllowAny,)

    def select_search(self, request, *args, **kwargs):
        """quick search for select"""
        name = request.query_params.get("q", "")
        size = request.query_params.get("size", 10)
        query_results = Team.objects.filter(
            name__contains=name)[:size].values()
        results = [{"label": r["name"], "value": r["team_id"]}
                   for r in query_results]
        return Response(results, status=status.HTTP_200_OK)
