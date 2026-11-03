from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .models import Post
from django.http import Http404
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags_in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
        'posts': posts,
        'tag': tag
                }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        post,
        status = Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__monyh=month,
        publish__day=day)

    comments = post.comments.filter(active= True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id' , flat=True)
    similar_posts = Post.published.filter(
        tags_in=post_tags_ids
    ).exclude(id=post_id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html '


def post_share(request, post_id):
    post = get_object_or_404(
        post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        form = EmailpostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.bluild_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'from': form,
            'sent': sent
        }
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None

    form = CommentForm(data=require_POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )


