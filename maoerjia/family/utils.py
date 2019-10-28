"""
Author: wangteng
"""

from collections import OrderedDict
from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
from django.utils import six
from apps.core.models import User


def json_response(data=None, error=None, message=None):
    """返回统一响应数据"""
    response_data = {"data": data, "message": message, "error": error}
    return response_data


class JsonResponse(Response):
    """
    统一返回HttpResponse数据
    用法: return JsonResponse(data=Json_data, message="message", error="error" status=status_code)
    """

    def __init__(self, data=None, message=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, error=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            message = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(message)

        self.data = {"error": error, "message": message, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


class GenToken:
    """
    生成或验证用户token
    """

    def __init__(self, email=None):
        self.email = email

    def generate_auth_token(self):
        s = Serializer(settings.SECRET_KEY, expires_in=settings.TOKEN_LIFETIME)
        return bytes.decode(s.dumps({'email': self.email}))

    def verify_auth_token(self, token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None, "用户token已过期"  # valid token, but expired
        except BadSignature:
            return None, "无效的token"  # invalid token
        email = data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return "无效的token"
        data["id"] = user.user_id
        return True, data


class StandardResultsSetPagination(LimitOffsetPagination):
    """
    自定义分页器
    """

    # 默认每页显示的数据条数
    default_limit = settings.PAGINATION_DEFAULT["length"]
    # URL中传入的参数  每页显示的数据条数
    limit_query_param = 'length'
    # URL中传入的参数  当前数据页码
    offset_query_param = 'page'
    # 最大每页显示条数
    max_limit = None

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        self.offset = self.offset * self.limit
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data, page_params="", length_params=""):
        if not page_params.isdigit():
            page_params = settings.PAGINATION_DEFAULT["page"]
        if not length_params.isdigit():
            length_params = int(settings.PAGINATION_DEFAULT["length"])
        if int(length_params) == 0:
            length_params = int(settings.PAGINATION_DEFAULT["length"])
        data = OrderedDict([
            ('pages', int((self.count+int(length_params)-1)/int(length_params))),
            ('current', int(page_params)),
            ('results', data)
        ])
        return data


def get_token_from_request(request):
    """
    从请求中获取token
    """
    token_generator = GenToken()
    auth_token = request.META.get(settings.TOKEN_HEADER, "")
    return token_generator.verify_auth_token(auth_token)
