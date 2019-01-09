from django.conf.urls import url
from application import views

app_name='application'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.login_user, name='login'),
    url(r'profile/(?P<course>[a-zA-Z]+)$', views.profile, name='profile'),
    url(r'profile_t/(?P<course>[a-zA-Z]+)$', views.profile_t, name='profile_t'),
    url(r'logout/$', views.logout_user, name='logout'),
    url(r'assignment/(?P<assign_id>[0-9]+)$', views.detail, name='detail'),
    url(r'assignment_t/(?P<assign_id>[0-9]+)$', views.detail_t, name='detail_t'),
    url(r'sol_detail_t/(?P<sol_id>[0-9]+)$', views.sol_detail_t, name='sol_detail_t'),
    url(r'submit/(?P<assignment_id>[0-9]+)$', views.submit, name='submit'),
    url(r'add_t/(?P<course>[a-zA-Z]+)$', views.add_t, name='add_t'),
    url(r't_courses',views.t_courses,name="t_courses"),
    url(r's_courses',views.s_courses,name="s_courses"),
]
