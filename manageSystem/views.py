import requests
from django.http import HttpResponse, JsonResponse
from manageSystem import DBMS
import json
import jwt

secret = 'secret'


def my_request(url, params, data_type='json'):
    headers = {'content-type': "application/" + data_type, 'token': '38dde2bc42dbdc386e85a7c697839ee5',
               'cache-control': 'no-cache'}
    response = requests.post(url, data=json.dumps(params), headers=headers)
    data = response.text.replace("\\\"", "\"")
    return data


def get_water_use(request):
    data = DBMS.Water().get_all_water_use()
    return JsonResponse({'code': 200, 'msg': '操作成功', 'data': data})


def get_water_amount(request):
    data = DBMS.Water().get_water_amount()
    return JsonResponse({'code': 200, 'msg': '操作成功', 'data': data})


# def forest(request):
#     # 长江经济带 - --上海市森林覆盖率
#     # woodland_area 林地面积【公顷】
#     # data_year 年度
#     # forest_rate 森林覆盖率【单位;百分比】
#     # land_area 土地面积【公顷】
#     data = my_request('https://data.sh.gov.cn/interface/10243/23733', {"data_year": "2021", "limit": 60, "offset": 0})
#     return HttpResponse(data)

def forest(request):
    data = DBMS.Tree().forest()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_production_average(request):
    data = DBMS.Population().get_production_average()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_permanent(request):
    data = DBMS.Population().get_permanent()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_production_total(request):
    data = DBMS.Population().get_production_total()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_job(request):
    data = DBMS.Population().get_job()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_pay_index(request):
    data = DBMS.Population().get_pay_index()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_pay_level(request):
    data = DBMS.Population().get_pay_level()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def cleanEnterprises(request):
    # 企事业信息公开 - 清洁生产企业年度名单
    # st_sc 是否双超企业
    # st_sy 是否双有企业
    # st_dwmc 单位名称
    # st_id 编号
    data = my_request('https://data.sh.gov.cn/interface/9442/23941', {"nm_year": "2021", "limit": 500, "offset": 0})
    print(data)
    return HttpResponse(data)


def get_pollution_company_list(request):
    data = DBMS.DataCenter().get_pollution_company_list()
    return JsonResponse({'code': 200, 'msg': '操作成功', 'data': data})


def get_pollution_sources(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        company_name = body['company_name']
        data = DBMS.DataCenter().get_pollution_sources(company_name)
        return JsonResponse({'code': 200, 'msg': '操作成功', 'data': data})


def get_industrial(request):
    data = DBMS.DataCenter().get_industrial()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_contraceptives(request):
    data = DBMS.DataCenter().get_contraceptives()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_contraceptives_detail(request):
    data = DBMS.DataCenter().get_contraceptives_detail()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_people(request):
    data = DBMS.DataCenter().get_people()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_income(request):
    data = DBMS.DataCenter().get_income()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_pay(request):
    data = DBMS.DataCenter().get_pay()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def login(request):
    if request.method == 'POST':
        body = request.body
        data = json.loads(body.decode())
        username = data['username']
        password = data['password']
        if username is None or password is None:
            return JsonResponse({'code': 500, 'msg': '请求参数错误'})
        is_login = DBMS.User().login(username=username, password=password)
        if not is_login:
            return JsonResponse({'code': 500, 'msg': '账号或密码错误'})
        token = jwt.encode(data, secret, algorithm='HS256')
        DBMS.User().set_token(username=username, token=token)
        return JsonResponse({'code': 200, 'msg': '操作成功', 'token': token, 'username': username, 'user_id': is_login})


def get_all_user(request):
    data = DBMS.User().get_all_user()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_all_user_part(request):
    data = DBMS.User().get_all_user_part()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def get_user_detail(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        data = DBMS.User().get_user_detail(body['id'])
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data)


def add_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        real_name = body['real_name']
        nick_name = body['nick_name']
        email = body['email']
        sex = int(body['sex'])
        phone_number = body['phone_number']
        password = body['password']
        role = int(body['role'])
        username = body['username']
        data = DBMS.User().add_user(real_name, nick_name, email, sex, phone_number, password, role, username)
        return HttpResponse('OK')


def update_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body['id']
        real_name = body['real_name']
        nick_name = body['nick_name']
        email = body['email']
        sex = int(body['sex'])
        phone_number = body['phone_number']
        password = body['password']
        role = int(body['role'])
        username = body['username']
        data = DBMS.User().update_user(id, real_name, nick_name, email, sex, phone_number, password, role, username)
        return HttpResponse('OK')


def delete_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body['id']
        data = DBMS.User().delete_user(id)
        return HttpResponse('OK')


def get_role_list(request):
    data = DBMS.Role().get_role_list()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def add_role(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        role_name = body['role_name']
        data = DBMS.Role().add_role(role_name)
        return HttpResponse('OK')


def update_role(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body['id']
        role_name = body['role_name']
        data = DBMS.Role().update_role(id, role_name)
        return HttpResponse('OK')


def delete_role(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(request.body)
        id = body['id']
        data = DBMS.Role().delete_role(id)
        return HttpResponse('OK')


def get_permission_list(request):
    data = DBMS.Permission().get_permission_list()
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def add_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        permission_name = body['permission_name']
        permission_path = body['permission_path']
        data = DBMS.Permission().add_permission(permission_name, permission_path)
        return HttpResponse('OK')


def update_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body['id']
        permission_name = body['permission_name']
        permission_path = body['permission_path']
        data = DBMS.Permission().update_permission(id, permission_name, permission_path)
        return HttpResponse('OK')


def delete_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body['id']
        data = DBMS.Permission().delete_permission(id)
        return HttpResponse('OK')


def bind_role_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        role_id = body['role_id']
        permission_list = body['permission_list']
        DBMS.RolePermission().bind_role_permission(role_id, permission_list)
        return HttpResponse('OK')


def get_role_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        role_id = body['role_id']
        data = DBMS.RolePermission().get_role_permission(role_id)
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data)


def bind_role_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        role_id = body['role_id']
        user_list = body['user_list']
        DBMS.RoleUser().bind_role_user(role_id, user_list)
        return HttpResponse('OK')


def get_role_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        role_id = body['role_id']
        data = DBMS.RoleUser().get_role_user(role_id)
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data)


def get_user_permission(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        data = DBMS.UserPermission().get_user_permission(user_id)
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data)


def get_routes(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body['user_id']
        data = DBMS.User().get_routes(user_id)
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data)