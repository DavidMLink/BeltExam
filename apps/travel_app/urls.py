from django.conf.urls import url
from . import views

urlpatterns = [
    # REGISTRATION AND LOGIN
    url(r'^$', views.index),
    url(r'^processRegister$', views.processRegister),
    url(r'^processLogin$', views.processLogin),
    url(r'^loginTemplate$', views.loginTemplate),
    url(r'^clearSession$', views.clearSession),
    # END OF REGISTRATION AND LOGIN

    # MAIN TRAVEL APPLICATION
    url(r'^loggedIn$', views.loggedIn),
    url(r'^addPlanTemplate$', views.addPlanTemplate),
    url(r'^create_plan$', views.create_plan),
    url(r'^joinPlan/(?P<plan_id>\d+)$', views.joinPlan),
    url(r'^show/(?P<plan_id>\d+)$', views.show),
    # END OF MAIN TRAVEL APPLICATION


]