# maoerjia系统

## 1. 开发环境

### 1.1 启动本地数据库

```shell

注意：从git拉下来代码后，首先删除掉family/migrations/目录下以000开头的数据库迁移文件， 再删除掉本地当前目录下db.sqlite3文件（如果有）

目前开发使用的sqlite3，以下创建mysql数据库过程忽略

创建本地数据库
CREATE DATABASE IF NOT EXISTS maoerjia DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
CREATE USER 'maoerjia'@'%' IDENTIFIED BY '12345678';
GRANT All privileges ON maoerjia.* TO 'maoerjia'@'%';

```

### 1.2 创建开发环境

```shell
git clone https://github.com/cncert/maoerjia.git
# cd maoerjia
# python37 -m venv venv
# source venv/bin/activate
(venv)# pip install -r requirements.txt
(venv)# cd maoerjia/
(venv)# python manage.py makemigrations
(venv)# python manage.py migrate
```

### 1.3 执行数据库迁移操作

每次从git更新代码后，都需要先执行以下操作

```shell
删除掉本地db.sqlite3数据库文件
删除掉family/migrations/目录下以000开头的数据库迁移文件
python manage.py makemigrations
python manage.py migrate
```

### 1.3 启动服务器

```shell
python manage.py runserver
```

## 2. 部署

```shell
mkdir -p /var/www/maoerjia/static
python manage.py collectstatic
```

部署需要安装 WSGI 兼容的 gunicore 作为 web 服务器, nginx 用于 serve 静态文件和作为反向代理服务器指向后端 django 服务.

## 3. 开发注意事项

### 3.1 更改model后，再执行数据库迁移操作

```shell
python manage.py makemigrations
python manage.py migrate
```

### 3.2 开发接口主要在family/api/main_view.py文件里
