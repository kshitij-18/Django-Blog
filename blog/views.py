from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import requests
import json
from .forms import ArticleForm
from .models import article, User
# Create your views here.


def home(request):
    return render(request, 'blog/index.html')


def register_request(request):
    if request.user.is_authenticated:
        return redirect('articlelist')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # recaptcha stuff
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6Lewz-IUAAAAAH0Egh_E5ozN1kS5aqT4vmvOO3r2'
        captchaData = {
            'secret': secretkey,
            'response': clientkey
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        if form.is_valid() and verify:
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('articlelist')
        else:
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('articlelist')
        else:
            return redirect('login')
    else:
        form = AuthenticationForm()
    frontend = {
        'form': form
    }
    return render(request, 'blog/login.html', frontend)


def logout_request(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to Login First')
        return redirect('login')
    logout(request)
    return render(request, 'blog/logout.html')


def article_create_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('homepage')
        else:
            return redirect('article_form')
    else:
        form = ArticleForm()
    frontend = {
        'form': form
    }
    return render(request, 'blog/articlecreate_form.html', frontend)


def article_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        articles = user.articles.all()
        front = {
            'articles': articles
        }
    return render(request, 'blog/article_list.html', front)


def search(request):
    username = request.GET.get('query')
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse('Looks like the user does not exist on our database')
    articles = user.articles.filter(category="Public")
    front = {
        'articles': articles,
        'username': username
    }
    return render(request, 'blog/searchlist.html', front)


def search_list(request):
    pass
