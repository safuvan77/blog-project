import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Comment
from .forms import BlogForm


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    blogs = Blog.objects.all()
    word=request.GET.get('keyword')
    if word:
        blogs=blogs.filter(content__icontains=word)
    context = {
            "blogs": blogs
    }
    return render(request, 'index.html', context)


def details(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        return redirect('home_page')

    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(
            text=text,
            ref_blog=blog,
            author=request.user
        )
        return redirect('blog_details', blog.id)

    comments = Comment.objects.filter(
        ref_blog=blog
    )
    context = {
        'blog': blog,
        'comments': comments
    }
    return render(request, 'blog_detail.html', context)


@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        t = request.POST.get('heading')
        c = request.POST.get('content')
        image = request.FILES.get('image')
        category=request.POST.get('category')
        Blog.objects.create(
            title=t,
            content=c,
            image=image,
            author=request.user,
            catogory=category
        )
        return redirect('home_page')
    context={
        'choices':Blog.categorise
    }

    return render(request, 'blog_create.html',context)


@login_required(login_url='login')
def edit(request, id):
    blog = Blog.objects.get(id=id)
    if request.user != blog.author:
        return HttpResponse('You are not authorize view this page !!!')

    if request.method == 'POST':
        t = request.POST.get('heading')
        c = request.POST.get('content')

        blog.title = t
        blog.content = c
        blog.save()
        return redirect('blog_details', blog.id)

    context = {
        'blog': blog
    }
    return render(request, 'blog_edit.html', context)


@login_required(login_url='login')
def delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('home_page')


def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    if request.user != comment.author:
        return HttpResponse('You are not authorize to access this page !!!')

    blog_id = comment.ref_blog.id
    comment.delete()
    return redirect('blog_details', blog_id)


def comment_edit(request, id):
    comment = Comment.objects.get(id=id)
    blog = comment.ref_blog

    if request.method == 'POST':
        t = request.POST.get('comment_text')
        comment.text = t
        comment.save()
        return redirect('blog_details', blog.id)
    comments = Comment.objects.filter(
        ref_blog=blog
    )
    context = {
        'blog': blog,
        'comments': comments,
        'cmt': comment,
        'edit': True
    }
    return render(request, 'blog_detail.html', context)


def article_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home_page')
        messages.error(request, form.errors)
    return render(request, 'blog_create_new.html')

