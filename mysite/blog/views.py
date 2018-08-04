from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Post
from .models import Comment
from .forms import CommentForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    object_list=Post.published.all()
    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/posts/list.html',{'page':page,
                                                  'posts':posts})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                           status='published',
                           publish__year=year,
                           publish__month=month,
                           publish__day=day)
    comments=post.comments.filter(active=True)

    if (request.method=='POST'):
        comment_form=CommentForm(data=request.POST)
        if(comment_form.is_valid()):
            new_comment=comment_form.save()
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    return render(request,'blog/posts/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'comment_form':comment_form})

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if(request.method=='POST'):
        form=EmailPostForm(request.POST)
        if(form.is_valid()):
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read "{}" at  {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'vimleshdixit007@gmail.com',[cd['to']])
            sent=True

    else:
        form=EmailPostForm()
    return render(request,'blog/posts/share.html',
                  {'post':post,
                   'form':form,
                   'sent':sent})
    
    
