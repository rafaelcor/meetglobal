#coding=utf-8

from django.http import HttpResponse

from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.mail import EmailMessage
from django.core.mail import send_mail


from page.models import User as Uuser
from page.models import UsersToConfirm


import json
import random
import base64
import smtplib
import re


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Create your views here.

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
        if re_correo.search(var["email"][0]):
            print 2
            ran = self.genRandomActivationSubfixLink(var["name"][0], var["email"][0])
                #print self.genRandomActivationSubfixLink(var["nombre"][0], var["correo"][0])
            reg = UsersToConfirm(
                                                    name=var["name"][0],
                                                    surname=var["surname"][0],
                                                    age=var["age"][0],
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


class LogOut(TemplateView):
    def get(self, request):
        logout(request)
        return super(LogOut, self).get(request)
    template_name = 'page/logout.html'

class EditProfileView(TemplateView):
    template_name = "page/editprofile.html"
    def split_semicolon(self):
        return self.split(";")

class AddLangRequest(View):
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
    
class GetLangRequest(View):
    def get(self, request, *args, **kwargs):
        userGet = User.objects.get(username=request.user)
        print userGet.language
        return HttpResponse(userGet.language)
        #return HttpResponse("{1:2}", content_type="application/json")

class RemoveLangRequest(View):
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
    
class SearchPeopleRequest(View):
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
                    users[user.username] = [langs, "%s %s"%(user.first_name, user.last_name)]
                    #print 456
        print request.user
        del users["%s"%request.user]
        return HttpResponse(json.dumps(users), content_type="application/json")

class SearchPeople(TemplateView):
    template_name = "page/searchpeople.html"

class upload(View):
    
    def post(self, request, *args, **kwargs):
        response_data = {}

        if request.is_ajax():
            form = UploaderForm(request.POST, request.FILES)

            if form.is_valid():
                upload = Upload(
                upload=request.FILES['upload']
                )
                upload.name = request.FILES['upload'].name
                upload.save()

                response_data['status'] = "success"
                response_data['result'] = "Your file has been uploaded:"
                response_data['fileLink'] = "/%s" % upload.upload

                return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data['status'] = "error"
        response_data['result'] = "We're sorry, but something went wrong. Please be sure that your file respects the upload                                                                                                                         conditions."

        return HttpResponse(json.dumps(response_data), content_type='application/json')
                    
        
