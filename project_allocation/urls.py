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
from rule_engine.rules_set import RuleSetEngineView 
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
]
