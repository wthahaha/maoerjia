# 1. 家庭及基本信息管理

## 1.1 查询家庭基本信息

```json
GET /api/home_basic_info/?search=""&page=""&length=""  [其中查询参数可选]


//其中
queryParams: {
 qkeys: string, (查询字段的组合, 以"+"连接字段，如："home_nick_name+home_of_city", 缺省为空)
 qvalue: string, (要查询的内容, 如： "root", 缺省为空)
 length: int, (每页显示的条数, 缺省为20)
 current: int (当前页数, 缺省为0)
}

RESPONSE 200: {
  message: "",
  data: {
      "pages": 1, (总页数)
      "current": 0, (当前页数)
      "results": [
          {
            "id": 1,
            "home_nick_name": "test",
            "home_of_city": "bj",
            "home_address_detail": "xxx",
            "home_facility": "xxx",
            "home_members_num": 1,
            "is_have_pet_zone": true,
            "is_have_old_man": true,
            "is_have_child": false
          }, {...}
      ],
  error: null
}

RESPONSE 4xx/5xx:{
  message: null,
  error: "xxx",
  data: null
}
```

```json
GET /api/home_basic_info/id

RESPONSE 200: {
  message: "",
  data: {
        "id": 1,
        "home_nick_name": "test",
        "home_of_city": "bj",
        "home_address_detail": "xxx",
        "home_facility": "xxx",
        "home_members_num": 1,
        "is_have_pet_zone": true,
        "is_have_old_man": true,
        "is_have_child": false
    }
  error: null
}

RESPONSE 4xx/5xx:{
  message: null,
  error: "xxx",
  data: null
}
```

## 2.1 创建家庭基本信息

```json
POST /api/home_basic_info/


Post:{
    "home_nick_name": "test", (必选，字符串)
    "home_of_city": "bj", (必选，字符串)
    "home_address_detail": "xxx", (必选，字符串)
    "home_facility": "xxx", (必选，字符串)
    "home_members_num": 1, (必选, 整数)
    "is_have_pet_zone": true, (必选，true or false)
    "is_have_old_man": true, (必选，true or false)
    "is_have_child": false (必选，true or false)
}

RESPONSE 201: {
  message: "创建成功"
  data: id
  error: null
}

RESPONSE 4xx/5xx:{
  message: null,
  error: "xxx",
  data: null
}
```

### 2.2 更新家庭基本信息

```json
PUT /api/home_basic_info/id


Post:{
    "home_nick_name": "test", (必选，字符串)
    "home_of_city": "bj", (必选，字符串)
    "home_address_detail": "xxx", (必选，字符串)
    "home_facility": "xxx", (必选，字符串)
    "home_members_num": 1, (必选, 整数)
    "is_have_pet_zone": true, (必选，true or false)
    "is_have_old_man": true, (必选，true or false)
    "is_have_child": false (必选，true or false)
}

RESPONSE 200: {
  message: "更新密钥成功"
  error: null
}

RESPONSE 4xx/5xx:{
  message: null,
  error: "xxx",
  data: null
}
```

### 2.3 删除家庭基本信息

```json
DELETE /api/home_basic_info/id


RESPONSE 200: {
  message: "删除成功"
  error: null,
  data: null
}

RESPONSE 4xx/5xx:{
  message: null,
  error: "xxx",
  data: null
}
```
