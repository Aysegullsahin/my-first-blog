from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.template.defaultfilters import slugify


from .enums import PostStatus
from .models import Post, Category
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status="Active")
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts':posts, 'categories': categories})

def post_detail(request,slug):
    post=Post.objects.get(slug=slug)
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'categories': categories, })

def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.slug = slugify(post.title)
            #post.status = PostStatus.AS_CHOICES
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.all()
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'categories': categories})    

def post_delete(request, slug):
    post = Post.objects.filter(slug=slug) 
    post.delete()
    return redirect(post_list)

def category_detail(request, slug):
    category = Category.objects.filter(slug=slug).first()
    categories = Category.objects.all()
    posts = category.post_set.filter(status="Active")
    temp =  {
        'category': category,
        'posts': posts,
        'categories': categories,
    }       
    return render(request, 'blog/post_list.html', temp)  








