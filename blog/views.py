from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DeleteView
#from django.utils.text import slugify

from .models import Post, Category
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts':posts, 'categories': categories})

def post_detail(request, pk,):
    post=Post.objects.get(pk=pk)
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
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})    

def post_delete(request, pk):
    post = Post.objects.filter(pk=pk) 
    post.delete()
    return redirect(post_list)

def category_detail(request, pk):
    category = Category.objects.filter(id=pk).first()
    posts = category.post_set.all()
    #slug = Category.objects.get(slug=slug)

    temp =  {
        'category': category,
        'posts': posts,
        #'slug': slug,
    }       
    return render(request, 'blog/post_list.html', temp)    



#import ipdb;
#ipdb.set_trace()






