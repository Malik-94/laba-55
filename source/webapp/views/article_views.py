from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.forms import ArticleForm, SimpleSearchForm
from webapp.models import Article, Tag


class IndexView(ListView):
    context_object_name = 'articles'
    model = Article
    template_name = 'article/index.html'
    ordering = ['created_at']
    paginate_by = 2
    paginate_orphans = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SimpleSearchForm(self.request.GET)
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        form = SimpleSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['search']
            if query:
                queryset = queryset.filter(Q(text__icontains=query)|Q(title__icontains=query))
        return queryset


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context



class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article/create.html'
    form_class = ArticleForm


    def form_valid(self, form):
        self.object = form.save()
        self.parser()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})

    def parser(self):
        tags = self.request.POST.get('tags')
        tag_list = tags.split(',')
        for tag in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(tag)



class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article/update.html'
    context_object_name = 'article'
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})

    def update_tag(self):
        tags = self.request.POST.get('tags')
        tags_list = tags.split(',')
        self.object.tags.clear()
        for tag in tags_list:
            get_tag, created_tag = Tag.objects.get_or_create(name=tag)
            self.object.tags.add(get_tag)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        query = self.object.tags.values('name')
        res = ''
        for tag in query:
            res += tag['name'] + ','
        print(res)
        print(query)

        form.fields['tags'].initial = res.replace(' ', '').strip(',')
        return form

    def form_valid(self, form):
        self.object = form.save()
        self.update_tag()
        return redirect(self.get_success_url())


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article/delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('index')