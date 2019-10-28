from rest_framework.views import exception_handler


ERROR_MSG = {
    "unique": "字段数据已存在",
    "blank": "字段不能为空",
    "required": "字段缺失",
}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        field_name = ""
        error = None
        try:
            for field_name in response.data:
                field_name = field_name
                error_code = response.data[field_name][0].code
                error = field_name + ": " + ERROR_MSG.get(error_code, str(response.data[field_name][0]))
        except:
            error = "未知异常"
        response.data.clear()
        response.data['message'] = None
        response.data['data'] = None
        if response.status_code == 404:
            try:
                response.data['error'] = response.data.pop('detail')
                response.data['error'] = "请求的资源不存在"
            except KeyError:
                response.data['error'] = "请求的资源不存在"

        if response.status_code == 400:
            response.data['error'] = error

        elif response.status_code == 401:
            response.data['error'] = "授权失败"

        elif response.status_code >= 500:
            response.data['error'] =  "服务器内部错误"

        elif response.status_code == 403:
            response.data['error'] = "访问拒绝"

        elif response.status_code == 405:
            response.data['error'] = 'HTTP请求方法错误'

    return response
