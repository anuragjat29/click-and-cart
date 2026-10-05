from django.shortcuts import render
from django.http import HttpResponse
from .models import BlogPost
# Create your views here.
def index(request):
    blogpost = BlogPost.objects.all()
    return render(request,'blog/index.html',{"posts" : blogpost})

def blogpost(requset, id):
    post = BlogPost.objects.get(post_id=id)
    print(post.title)
    print(post.head0," tt")

    return render(requset, 'blog/blogpost.html',{"posts":post})