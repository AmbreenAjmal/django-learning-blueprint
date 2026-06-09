from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from .models import Post

@cache_page(60)
def post_list(request):
    posts = Post.published_posts.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            published=True
        )
        send_mail(
            subject=f'New post published: {post.title}',
            message=f'{post.author} just published a new post.\n\n{post.content}',
            from_email='blog@djangolearning.com',
            recipient_list=['admin@djangolearning.com'],
        )
        return redirect('post_list')
    return render(request, 'blog/post_form.html')