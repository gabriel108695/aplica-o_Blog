from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm


# Create your views here.

def post_list(request):
    post_list = Post.published.all()
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
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        post,
        status = Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__monyh=month,
        publish__day=day)
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
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
    queryset = post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list. html '


def post_share(request, post_id):
    post = get_object_or_404(
        post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method == 'POST':
        form = EmailpostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'from': form
        }
    )


