"""project_allocation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rule_engine.views import RuleEngineView, CommonMasterView
from account.views import UserOperationView
from account.userGroup import UserGroupsView
from rule_engine.rules_set import RuleSetEngineView
from connection.views import ConnectionHistoryView, ConnectionViewSet, NlpAnalysisView
from rule_engine.RuleConfigurations import RuleEngineConfigurationsView,RuleEngineConfigurationConditionsView,RuleEngineConfigurationValueView,RuleEngineGroupsView,RuleEngineFunctionalOperationView,RuleEngineAuditView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('common/list/', CommonMasterView.as_view({'post': 'list'})),

    path('rule/engine/list/', RuleEngineView.as_view({'post': 'list'})),
    path('rule/engine/create/', RuleEngineView.as_view({'post': 'create'})), 
    path('rule/engine/view/', RuleEngineView.as_view({'post': 'view'})),  
    path('rule/engine/delete/', RuleEngineView.as_view({'post': 'delete'})),
    path('rule/engine/update/', RuleEngineView.as_view({'post': 'update'})), 

    path('rule/set/list/', RuleSetEngineView.as_view({'post': 'list'})),
    path('rule/set/create/', RuleSetEngineView.as_view({'post': 'create'})), 
    path('rule/set/view/', RuleSetEngineView.as_view({'post': 'view'})),  
    path('rule/set/delete/', RuleSetEngineView.as_view({'post': 'delete'})),
    path('rule/set/update/', RuleSetEngineView.as_view({'post': 'update'})), 

    path('connection/', ConnectionViewSet.as_view({'get': 'list'})),
    path('connection/create/', ConnectionViewSet.as_view({'post': 'create'})),
    path('connection/new/', ConnectionViewSet.as_view({'get': 'new'})),
    path('connection/update/<connection_id>', ConnectionViewSet.as_view({'put': 'update'})),
    path('connection/delete/<connection_id>', ConnectionViewSet.as_view({'delete': 'delete'})),
    path('connection/view/<connection_id>', ConnectionViewSet.as_view({'get': 'view'})),
    path('connection/test', ConnectionViewSet.as_view({'post': 'test_connection'})),
    path('connection/datamap/view/<connection_id>', ConnectionViewSet.as_view({'get': 'datamap_view'})),
    path('connection/list/', ConnectionViewSet.as_view({'post': 'connection_list'})),
    path('connection/history/list', ConnectionHistoryView.as_view({'post': 'list'})),

    path('users/create/', UserOperationView.as_view({'post':'create'})), # in default django user
    path('users/update/', UserOperationView.as_view({'post':'update'})),
    path('users/delete/', UserOperationView.as_view({'post':'delete'})),
    path('users/list/', UserOperationView.as_view({'post':'list'})),
    path('users/view/', UserOperationView.as_view({'post':'view'})),
    path('users/changepassword/', UserOperationView.as_view({'post':'changepassword'})),

    path('users/creategroup/', UserGroupsView.as_view({'post':'create'})), # in default django user group
    path('users/updategroup/', UserGroupsView.as_view({'post':'update'})),
    path('users/deletegroup/', UserGroupsView.as_view({'post':'delete'})),
    path('users/grouplist/', UserGroupsView.as_view({'post':'list'})),
    path('users/groupview/', UserGroupsView.as_view({'post':'view'})),
    path('users/addtogroup/', UserGroupsView.as_view({'post':'addToGroup'})),
    path('users/removegroup/', UserGroupsView.as_view({'post':'removeGroup'})),

    path('rule/functionOperation/create/', RuleEngineFunctionalOperationView.as_view({'post':'create'})),
    path('rule/functionOperation/update/', RuleEngineFunctionalOperationView.as_view({'post':'update'})),
    path('rule/functionOperation/delete/', RuleEngineFunctionalOperationView.as_view({'post':'delete'})),
    path('rule/functionOperation/list/', RuleEngineFunctionalOperationView.as_view({'post':'list'})),
    path('rule/functionOperation/view/', RuleEngineFunctionalOperationView.as_view({'post':'view'})),
    path('rule/functionOperation/viewby/', RuleEngineFunctionalOperationView.as_view({'post':'viewby'})),

    path('rule/configurations/create/', RuleEngineConfigurationsView.as_view({'post':'create'})),

    path('rule/configurationCondition/create/', RuleEngineConfigurationConditionsView.as_view({'post':'create'})),

    path('rule/configurationValue/create/', RuleEngineConfigurationValueView.as_view({'post':'create'})),

    path('rule/group/create/', RuleEngineGroupsView.as_view({'post':'create'})),

    path('rule/audit/create/', RuleEngineAuditView.as_view({'post':'create'})),


    



]
