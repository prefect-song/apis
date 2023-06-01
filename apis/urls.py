"""
URL configuration for apis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from manageSystem import views

urlpatterns = [
    path('login', views.login),
    path('routes/get', views.get_routes),

    path('water/supply', views.get_water_use),
    path('water/amount', views.get_water_amount),

    path('forest', views.forest),

    path('pollution/company/query', views.get_pollution_company_list),
    path('pollution/query', views.get_pollution_sources),
    path('cleanEnterprises', views.cleanEnterprises),

    path('user/query', views.get_all_user),
    path('user/part', views.get_all_user_part),
    path('user/detail', views.get_user_detail),
    path('user/add', views.add_user),
    path('user/delete', views.delete_user),
    path('user/update', views.update_user),

    path('role/list', views.get_role_list),
    path('role/add', views.add_role),
    path('role/delete', views.delete_role),
    path('role/update', views.update_role),

    path('permission/list', views.get_permission_list),
    path('permission/add', views.add_permission),
    path('permission/delete', views.delete_permission),
    path('permission/update', views.update_permission),

    path('role/permission/bind', views.bind_role_permission),
    path('role/permission/get', views.get_role_permission),

    path('role/user/bind', views.bind_role_user),
    path('role/user/get', views.get_role_user),

    path('user/permission/get', views.get_user_permission),

    path('industrial/get', views.get_industrial),
    path('contraceptives/get', views.get_contraceptives),
    path('contraceptives/detail/get', views.get_contraceptives_detail),
    path('people/get', views.get_people),
    path('income/get', views.get_income),
    path('pay/get', views.get_pay),
    path('average/get', views.get_production_average),
    path('permanent', views.get_permanent),
    path('productionTotal', views.get_production_total),
    path('job', views.get_job),
    path('payIndex', views.get_pay_index),
    path('payLevel', views.get_pay_level),
]