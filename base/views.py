from django.shortcuts import render, redirect
from .models import CustomUser, Topic, Articles, Messages
from .forms import CommentForm, CustomUserCreationForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
import os

def home(request):
    page = 'home'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()
    articles = Articles.objects.filter(Q(topic__name__icontains=q) | Q(title__icontains=q))
    context = {'topics': topics, 'articles': articles, 'page': page}
    return render(request, 'base/home.html', context)
    
class Loginpage(View):

    def get(self,request, *args, **kwargs):
        page = 'login'
        context = {'page': page}
        return render(request, 'base/login_register.html', context) 

    def post(self,request, *args, **kwargs):
        page = 'login'
        context = {'page': page}
        if request.user.is_authenticated:
            return redirect('home')

        password = request.POST.get('password')

        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', context)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Email or password is invalid')
        return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')


def sendEmail(request, user, template, **extra_fileds):

    if user is not None:
        current_site = get_current_site(request)
        mail_subject = extra_fileds.get('subject')
        message = render_to_string(template,
        {'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        })
        to_email = extra_fileds.get('mail_address')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return True
    return False


def forgotPassword(request):
    page = 'forgot-password'
    subject = 'Reset password'
    template_name = 'base/reset_password_email.html'
    context = {'page': page }
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=user_email)
        except:
            user = None
        bool = sendEmail(request, user, template_name, mail_address = user_email, subject = subject)
        if bool:
            return render(request, 'base/sent_email.html', context)
    return render(request, 'base/forgot_password.html', context)

class Registerpage(View):
    page = 'register'
    template_name = 'base/activate_email.html'
    subject = 'Activate account.'
    form = CustomUserCreationForm()
    def get(self, request, *args, **kwargs):
        context = {'page': self.page, 'form': self.form}
        return render(request, 'base/login_register.html', context)
        
    def post(self, request, *args, **kwargs):
        subject = 'Activate account.'
        self.form = CustomUserCreationForm(request.POST)
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.is_active = False
            user.save()
            verify_mail = self.form.cleaned_data.get('email')
            bool = sendEmail(request, user, self.template_name, mail_address=verify_mail, subject = subject)
            if bool:
                return render(request, 'base/sent_email.html')
        else:
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            name = request.POST.get('username')
            if len(name) == 0:
                messages.error('You must enter username')
            if pass1 != pass2:
                messages.error(request, 'Password does not match')
            else:
                messages.error(request,'Password does not meet credentials')
            
        context = {'page': self.page, 'form': self.form}
        return render(request, 'base/login_register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid) 
    except(TypeError, ValueError):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid')

def resetPassword(request, uidb64, token):
    form = SetPasswordForm(request.user)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'base/password_reset_done.html', {'reseted': True})
            else:
                pass1 = request.POST.get('new_password1')
                pass2 = request.POST.get('new_password2')
                if pass1 != pass2:
                    messages.error(request,"Password doesn't match")
        context = {'form': form}
        return render(request, 'base/reset_password.html', context)
    else:
        return HttpResponse('Invalid link')


class Articlepage(View):

    def get(self, request, title, *args, **kwargs):

        article = Articles.objects.get(title=title)
        comments = article.messages_set.all()
        likes_count = article.likes.count()
        liked = False
        if article.likes.filter(id=request.user.id).exists():
            liked = True
        comment_form = CommentForm()
        context = {'article': article, 'comments': comments,  'likes': likes_count, 'liked': liked, 'form': comment_form}
        return render(request, 'base/main_article.html', context)


    def post(self, request, title, *args, **kwargs):
        article = Articles.objects.get(title=title)
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data.get('body')
            success = False
            if body:
                success = True
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            result = comment_form.cleaned_data.get('body')
            user = request.user.username
            return JsonResponse({'result': result, 'user': user, 
            'comment_id': comment.id, 
            'image': comment.user.user_avatar.url, 
            'success': success})
        
        return redirect('article', title=article.title)
        

def like(request):
    liked = False
    if request.method == 'POST':
        pk = int(request.POST.get('post_id'))
        article = Articles.objects.get(id=pk)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            liked = False
        else:
            liked = True
            article.likes.add(request.user)
        context = {'total_likes': article.likes.count(), 'liked': liked}
        return JsonResponse(context,safe=False)
    

def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)
    articles = Articles.objects.filter(host=user)
    context = {'articles': articles, 'user': user}
    return render(request, 'base/user_profile.html', context)

@login_required(login_url='login')
def userSettings(request):
    title = 'Account Settings'
    user = request.user
    form = UserUpdateForm(instance=user)
    context = {'form': form, 'title': title}
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        old_image = request.user.user_avatar
        if form.is_valid():
            if request.FILES.get('user_avatar') is not None and os.path.exists(old_image.path):
                os.remove(old_image.path)
            form.save()
            return redirect('home')
    return render(request, 'base/account_setting.html', context)

@login_required(login_url='login')
def updatePassword(request):
    title = 'Update Password'
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            logout(request)
        return redirect('login')
    context = {'form': form, 'title': title}
    return render(request, 'base/update_password.html', context)

@login_required(login_url='login')
def deleteComment(request):
    pk = request.POST.get('deletedcomment')
    comment = Messages.objects.get(id=pk)
    deleted = False
    if request.method == 'POST':
        comment.delete()
        deleted = True
    context = {'deleted': deleted, 'id': pk}
    return JsonResponse(context)