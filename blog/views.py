from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .form import PubBlogForm
from django.db.models import Q


# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={'blogs':blogs})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': 'success', 'data': {'blog_id': blog.id}})

        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'message': 'fail'})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    # reload the detail after successfully post comment
    return redirect(reverse('blog:blog_detail', kwargs={"blog_id": blog_id}))


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    # search from both title and content
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request,'index.html', context={"blogs":blogs})

