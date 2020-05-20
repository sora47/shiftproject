from django.urls import path
from .views import login_func, signup_func, top_func, logout_func, registshift_func, registshiftbase_func, \
    choiceshift_func, viewshift_func, deleteuser_func, changestaff_func

urlpatterns = [
    path('signup/', signup_func, name='signup'),
    path('login/', login_func, name='login'),
    path('logout/', logout_func, name='logout'),
    path('top/', top_func, name='top'),
    path('regist/<int:year>/<int:month>/', registshift_func, name='registshift'),
    path('shiftbase/<int:year>/<int:month>/', registshiftbase_func, name='registshiftbase'),
    path('choice/<int:year>/<int:month>/', choiceshift_func, name='choiceshift'),
    path('shift/<int:year>/<int:month>/', viewshift_func, name='viewshift'),
    path('delete/', deleteuser_func, name='delete'),
    path('changestaff/', changestaff_func, name='changestaff')
]
