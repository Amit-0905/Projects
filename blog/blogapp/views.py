from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Post,Feedback
from datetime import datetime

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    random_images = [f'img/{i}.jpg' for i in range(1, 6)]
    context = {
        'posts' : posts,
        'blog_title' : 'Blogepedia By Amit',
        'year' : datetime.now().year,
        'random_images': random_images,
    }
    return render(request,'index.html',context)

def about(request):
    context = {
        'blog_title' : 'Blogepedia By Amit',
        'year' : datetime.now().year
    }
    return render(request,'about.html',context)

def contact(request):
    context = {
        'blog_title' : 'Blogepedia By Amit',
        'year' : datetime.now().year
    }
    return render(request,'contact.html',context)

def post_detail(request,post_id):
    context = {
        'blog_title' : 'Blogepedia By Amit',
        'year' : datetime.now().year,
        'post' : get_object_or_404(Post, id=post_id),
        # 'post' : Post.objects.get(id=post_id),
        'random_images' : [f'img/{i}.jpg' for i in range(1, 6)]
    }
    return render(request,'post.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Username or Password!')
            return redirect('login')
    else :
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')

        if password == cnf_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists. ')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists. ')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Passwords does not match.')
            return redirect('register')

    else:
        return render(request,'register.html')


def new_post(request):
    if request.user.is_superuser:
        context = {
        'blog_title' : 'Blogepedia By Amit',
        'year' : datetime.now().year
        }
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            published_date = datetime.now()
            if not title :
                messages.info(request,'Title is required.')
                return redirect('new_post')
            else:
                post = Post.objects.create(title=title,content=content,published_date=published_date)
                post.save()
                return redirect('/')
        else:
            return render(request,'new_post.html',context)
    else :
            messages.info(request,'You are not authorized to create a new post.Please login as staff to create post.')
            return redirect('login')

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        feedback = Feedback.objects.create(name=name,email=email,message=message)
        feedback.save()
        messages.success(request, 'Your message has been successfully sent!')
        return redirect('contact')
    else:
        return render(request, 'contact.html')