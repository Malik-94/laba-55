from django.shortcuts import render, get_list_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import CommentForm
from webapp.models import Comment


class CommentIndex(TemplateView):
    template_name = 'comment.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context



class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article']
            )
            # это нужно исправить на ваш url.
            return redirect('article_view', pk=comment.article.pk)
        else:
            return render(request, 'comment/create.html', context={'form': form})
