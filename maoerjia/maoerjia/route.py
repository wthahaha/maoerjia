"""
视图方法与http方法对应关系
"""

from family.api import main_view


# 主机认证视图
HomeBasicInfo_LIST = main_view.HomeBasicInfoView.as_view({
    'get': 'list',
    'post': 'create'
})

HomeBasicInfo_DETAIL = main_view.HomeBasicInfoView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

