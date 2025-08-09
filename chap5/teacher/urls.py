from django.urls import path
from teacher.views import student_view_form,teacher_view_form, home,profile,set_cookie, get_cookie, del_cookie,set_session,get_session,del_session


urlpatterns = [
    path('studentreg/', student_view_form, name='studentreg'),
    path('teacherreg/', teacher_view_form, name='teacherreg'),
    path('', home, name='home'),
    path('profile/<int:student_id>', profile, name='profile'), #dynamic url and int is used for striction of id only
 #slug will be used for larger string 
    path('set_cookie/', set_cookie, name='set_cookie'),
    path('get_cookie/', get_cookie, name='get_cookie'),
    path('del_cookie/', del_cookie, name='del_cookie'),
    path('set_session/', set_session, name='set_session'),
    path('get_session/', get_session, name='get_session'),
    path('del_session/', del_session, name='del_session'), 
]                                                              



