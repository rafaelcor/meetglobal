from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from page.views import Home
from page.views import Register
from page.views import Login
from page.views import RegisterRequestView
from page.views import ActivationView
from page.views import AboutUs
from page.views import LoginRequestView
from page.views import LogOut
from page.views import EditProfileView
from page.views import AddLangRequest
from page.views import GetLangRequest
from page.views import RemoveLangRequest

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'meetglobo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view()),
    url(r'^register/$', Register.as_view()),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', LogOut.as_view()),
    url(r'^editprofile', EditProfileView.as_view()),
    url(r'^aboutus/$', AboutUs.as_view()),
    url(r'^register_request/$', RegisterRequestView.as_view()),
    url(r'^activation/(?P<suffix>[a-zA-Z1-9=.,*]+)$', ActivationView.as_view()),
    url(r'^login_request/$', LoginRequestView.as_view()),
    url(r'^addLang_request/$', AddLangRequest.as_view()),
    url(r'^getLang_request/$', GetLangRequest.as_view()),
    url(r'^removeLang_request/$', RemoveLangRequest.as_view()),
)
