"""
视图方法与http方法对应关系
"""

from apps.core.api import main_view


# 主机认证视图
CREDENTIALS_LIST = main_view.SecureyKeyView.as_view({
    'get': 'list',
    'post': 'create'
})

CREDENTIALS_DETAIL = main_view.SecureyKeyView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

TEAM_LIST = main_view.TeamView.as_view({
    'get': 'list',
    'post': 'create'
})

TEAM_DETAIL = main_view.TeamView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

TEAM_SEARCH = main_view.TeamView.as_view({
    'get': 'select_search'
})
