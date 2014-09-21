#coding=utf-8

from django.http import HttpResponse

from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.core.mail import send_mail


from page.models import User as Uuser
from page.models import UsersToConfirm

from django.shortcuts import render, redirect #puedes importar render_to_response
from page.forms import UploadForm
from page.models import Document

import json
import random
import base64
import smtplib
import re
import os

from datetime import date
from calendar import monthrange


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Create your views here.

###Mixins
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CsrfExemptMixin(object):
    """
    Exempts the view from CSRF requirements.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)
###


class Home(TemplateView):
    template_name = "page/index.html"


class Register(TemplateView):
	template_name = "page/register.html"


class Login(TemplateView):
	template_name = "page/login.html"


class AboutUs(TemplateView):
	template_name = "page/aboutus.html"


class RegisterRequestView(View):
    def send_mail(self, receiver, link_sub, name):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        #Next, log in to the server
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("rafael.cordano@gmail.com", "todo4.es.tl")
        #Send the mail
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Activación"
        msg['From'] = "rafael.cordano@gmail.com"
        msg['To'] = receiver
        html = """\
                <html>
                  <head></head>
                  <body>
                    Bienvenido {1}!<br>
                    Tu cuenta está en proceso de verificación,<br>
                    por favor ingrese a este <a href="{0}">link</a> para activarla.<br>
                    <br>
                    Saludos<br>
                    <br>
                    El equipo de Meet Global
                  </body>
                </html>
                """.format("http://localhost:8000/activation/%s"%link_sub, name)
        msg.attach(MIMEText(html, 'html'))
        server.sendmail("rafael.cordano@gmail.com", receiver, msg.as_string())

    def genRandomActivationSubfixLink(self, auser, correo):
        var = "{0}{1}{2}".format(auser, correo, random.randint(1,100))
        ran = base64.b64encode(var)
        print "test"
        print ran
        return ran

    def post(self, request, *args, **kwargs):
        toresponse = 0
        re_correo = re.compile('^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        var = dict(request.POST)
        print var["date_of_birth"][0]
        if re_correo.search(var["email"][0]):
            print 2
            ran = self.genRandomActivationSubfixLink(var["name"][0], var["email"][0])
                #print self.genRandomActivationSubfixLink(var["nombre"][0], var["correo"][0])
            reg = UsersToConfirm(
                                                    name=var["name"][0],
                                                    surname=var["surname"][0],
                                                    dateOfBirth=var["date_of_birth"][0],
                                                    email=var["email"][0],
                                                    country=var["country"][0],
                                                    password=var["password"][0],
                                                    random_link_subfix=ran)
            reg.save()
            print ran
            self.send_mail(var["email"][0], ran, var["name"][0])
                #print self.genRandomActivationSubfixLink(var["nombre"][0], var["correo"][0])

            toresponse = {"register": "successful"}
        else:
            toresponse = {"register": "wrong"}
        return HttpResponse(json.dumps(toresponse), content_type="application/json")


class ActivationView(TemplateView):
    template_name = "page/activate.html"

    def get_context_data(self, **kwargs):
        toreturn = 0
        try:
            print 1
            context = super(ActivationView, self).get_context_data(**kwargs)
            print 2
            print context["suffix"]
            print 3
            getData = UsersToConfirm.objects.filter(random_link_subfix=context["suffix"])
            print 4
            create = User.objects.create_user(first_name=getData[0].name,
            								  last_name=getData[0].surname,
            								  date_of_birth=getData[0].dateOfBirth,
            								  country=getData[0].country,
            								  username=getData[0].email,
                                              password=getData[0].password,
                                              email=getData[0].email)
            print 5
            create.save()
            print 6
            getData.delete()
            print 7
        except Exception,e:
            toreturn = 1
            print 12
            print str(e)
        #print hola[0].name
        #return context
        return context


class AboutUs(TemplateView):
    template_name = "page/aboutus.html"


class LoginRequestView(View):

    def post(self, request, *args, **kwargs):
        self.user_session = None
        self.usdj = None
        var = dict(request.POST)
        self.user = var["email"][0]
        self.password = var["password"][0]
        return self.Signinf(request)

    def Signinf(self, request):
        usera = None
        var = {}
        usera = authenticate(username=self.user, password=self.password)
        if usera is None:
            var = {'login': 'wrong', 'user': self.user}
        else:
            if usera.is_active:
                login(request, usera)
                var = {'login': 'successful', 'user': self.user}

        return HttpResponse(json.dumps(var), content_type="application/json")


class LogOut(LoginRequiredMixin, TemplateView):
    def get(self, request):
        logout(request)
        return super(LogOut, self).get(request)
    template_name = 'page/logout.html'


class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = "page/editprofile.html"

    def split_semicolon(self):
        return self.split(";")


class AddLangRequest(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        var = dict(request.POST)
        self.langToAdd = var["language"];
        print self.langToAdd[0]
        userGet = User.objects.get(username=request.user)
        print userGet.language

        if userGet.language == "":
            userGet.language = "%s" % (self.langToAdd[0])
        else:
            userGet.language = "%s;%s" % (userGet.language, self.langToAdd[0])

        #print userGet.language == ""
        userGet.save()
        return HttpResponse(json.dumps(request.POST), content_type="application/json")


class GetLangRequest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        userGet = User.objects.get(username=request.user)
        print userGet.language
        return HttpResponse(userGet.language)
        #return HttpResponse("{1:2}", content_type="application/json")


class RemoveLangRequest(LoginRequiredMixin, View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        var = dict(request.POST)
        userGet = User.objects.get(username=request.user)
        userGet.language = userGet.language.replace(var["lang"][0], "").replace(";;", ";").replace(" ", "")
        print "-%s-"%userGet.language
        try:
            if userGet.language[-1] == ";":
               userGet.language = userGet.language[0:len(userGet.language)-1]
            elif userGet.language[0] == ";":
               userGet.language = userGet.language[1:len(userGet.language)]
        except:
            pass
        userGet.save()
        return HttpResponse(userGet.language)


class SearchPeopleRequest(LoginRequiredMixin, View):
    def age(self, day, month, year, cday=0, cmonth=0, cyear=0):
        date(year, month, day)
        if cday:
            today = date(cyear, cmonth, cday)
        else:
            today = date.today()
        years = today.year-year
        months = today.month-month
        days = today.day-day
        if days < 0:
            months -= 1
            days += monthrange(year, month)[1]
        if months < 0:
            years -= 1
            months += 12
        if years < 0:
            raise ValueError, "the given date wasn't reached yet!"
        return days, months, years

    def get(self, request, *args, **kwargs):
        userGet = User.objects.get(username=request.user)
        users = {}
        for langs in userGet.language.split(";"):
            print langs
            for user in User.objects.all():
                print user.language
                print langs
                if re.search(langs, user.language):
                    #print 123
                    print user.date_of_birth.year
                    users[user.username] = [langs, "%s %s"%(user.first_name,
                                                            user.last_name),
                                            self.age(user.date_of_birth.day, user.date_of_birth.month, user.date_of_birth.year)[2]]
                    #print 456
        print request.user
        del users["%s"%request.user]
        return HttpResponse(json.dumps(users), content_type="application/json")


class SearchPeople(LoginRequiredMixin, TemplateView):
    template_name = "page/searchpeople.html"


class UploadRequest(CsrfExemptMixin, LoginRequiredMixin, View):
    #def __init__(self, test):
    #    print

    def post(self, request, *args, **kwargs):
        var = dict(request.POST)
        if (not str(request.FILES["docfile"]).lower().endswith(".gif")) and (not str(request.FILES["docfile"]).lower().endswith(".jpg")) and (not str(request.FILES["docfile"]).lower().endswith(".jpeg")) and (not str(request.FILES["docfile"]).lower().endswith(".png")):
            return HttpResponse("<html><head><title>File Upload</title></head><body><b>The image must be .gif, .jpg, .jpeg or .png</b></body></html>", content_type="text/html")
        userGet = User.objects.get(username=request.user)
        print userGet.email
        print var["smg"]
        newdoc = Document(filename=userGet.email, docfile=request.FILES['docfile'])
        print 2
        newdoc.save()
        print request.FILES["docfile"]
        h = "media/imgProfiles/%s"%request.FILES['docfile']
        h2 = "media/imgProfiles/%s"%userGet.email
        print h
        os.rename(h, h2)
        #newdoc.save()
        print 3
        return HttpResponse(json.dumps(userGet.email), content_type="application/json")
    """
    def get(self, request, *args, **kwargs):
        docfildocfildocfildocfileeeeform = UploadForm()
        return render(request, 'page/editprofile.html', {
            'form': form
        })
    """
