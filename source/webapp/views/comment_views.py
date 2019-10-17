from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from webapp.forms import CommentForm
from webapp.models import Comment
from .base_views import ListView


class CommentListView(ListView):
    context_key = 'comments'
    model = Comment
    template_name = 'comment/index.html'


class CommentIndex(TemplateView):
    template_name = 'comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context



class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comment/create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/update.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})
