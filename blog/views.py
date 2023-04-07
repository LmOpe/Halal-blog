from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag

# Create your views here.

"""
Create FBV for retrieving all the published posts
"""
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
    {'posts': posts,
    'tag': tag})

"""
Create FBV for retrieving a single post
"""
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED, 
                            slug=post, 
                            publish__year=year, 
                            publish__month=month, 
                            publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', 
    {'post': post,
    'comments': comments,
    'form': form})

"""
 Create FBV for post comment
"""
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post': post,
                            'form': form,
                            'comment': comment})