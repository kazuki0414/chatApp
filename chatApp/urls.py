from django.urls import path
from chatApp.views import loginfunc,signupfunc,mainviewfunc,createProfilefunc,friendSearchfunc,friendRegifunc,friendsListViewfunc,friendTalkingfunc,logoutfunc,messageSubmitfunc

urlpatterns = [
    path('login/',loginfunc, name='login'),
    path('signup/',signupfunc, name='signup'),
    path('main/',mainviewfunc, name='main'),
    path('createProfile/',createProfilefunc, name='createProfile'),
    path('friendSearch/',friendSearchfunc, name='friendSearch'),
    path('friendregister/<int:pk>',friendRegifunc, name='friendregister'),
    path('friendslist/',friendsListViewfunc, name='friendslist'),
    path('friendTalking/<int:pk>',friendTalkingfunc, name='friendTalking'),
    path('logout/',logoutfunc, name='logout'),

]