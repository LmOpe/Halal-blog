from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

"""
Create FBV for retrieving all the published posts
"""
def post_list(request):
    posts = Posts.published.all()
    return render(request, 'blog/post/list.html',
    {'posts': posts})

"""
Create FBV for retrieving a single post
"""
def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', 
    {'post': post})