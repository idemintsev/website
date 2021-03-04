from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from news.forms import RegisterForm, CommentForm, NewsForm
from news.models import Profile, News, Comment, Tag


def register_user(request):
    """
    Регистрация пользователя
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                phone_number=phone,
                city=city
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('interfax')
    else:
        form = RegisterForm()
    return render(request, 'users/registration.html', {'form': form})


class NewsListView(generic.ListView):
    """
    Отражает список всех новостей.
    Если в request.GET.get('sorted_by') приходит имя тега, то отражает список всех новостей, содержащих данный тег.
    """
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        if self.request.GET.get('sorted_by'):
            tag_name = self.request.GET.get('sorted_by')
            queryset = News.objects.filter(tags__name=tag_name)
            return queryset
        queryset = super().get_queryset()
        return queryset


class NewsDetailsView(generic.DetailView):
    """
    Конкретная новость с формой для комментариев.
    Если пользователь не зарегистрирован на сайте, то в форме комментария значение в поле Имя заменяется на "Аноним".
    Для аутентифицированного пользователя автоматически подставляется его username, а поле Имя скрыто.
    """
    model = News
    form_class = NewsForm

    def get(self, request, *args, **kwargs):
        news = self.get_object()
        comments_form = CommentForm()
        if request.user.is_authenticated:
            comments_form.fields['name'].widget = forms.HiddenInput()
            comments_form.initial['name'] = request.user.username

        return render(request, 'news/news_details.html',
                      {'news_details': news,
                       'comments_form': comments_form}
                      )

    def post(self, request, pk):
        news = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = Comment(news=news, **comment_form.cleaned_data)
            if request.user.is_authenticated:
                new_comment.name = request.user.username
            else:
                new_comment.name = 'Аноним'
            new_comment.save()
        return HttpResponseRedirect(reverse('news_details', args=[pk]))


class AuthView(LoginView):
    """
    Аутентификация.
    После успешной аутентификации пользователь перенаправляется на страницу с новостями.
    """
    template_name = 'users/login.html'
    next_page = reverse_lazy('interfax')


class Logout(LogoutView):
    """
    Выхдод из своей учетной записи.
    После выхода пользователь перенаправляется на страницу с новостями.
    """
    template_name = 'users/logout.html'
    next_page = reverse_lazy('interfax')


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    """
    Профайл пользователя.
    Передает в шаблон данные авторизованного пользователя.
    Если пользователь не атворизован - перенаправляет на 'interfax'.
    """
    model = User
    redirect_field_name = 'interfax'

    def get(self, request, *args, **kwargs):
        profile_details = request.user
        access_to_create_news = profile_details.has_perm('news.add_news')
        previous_page = request.GET.get('next')
        if previous_page is None:
            previous_page = '/interfax/'
        return render(request, 'users/profile.html',
                      {'profile_details': profile_details, 'previous_page': previous_page,
                       'access_to_create_news': access_to_create_news},
                      )


class NewsCreateFormView(generic.CreateView):
    """
    Создание новостей.
    В post-запросе из шаблона create_news.html принимает заголовок и текст новости, а также тег, если он указан при
    создании новости.
    """
    form_class = NewsForm
    template_name = 'news/create_news.html'

    def post(self, request, *args, **kwargs):
        tags = request.POST.get('tags')
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            news = News(**news_form.cleaned_data)
            news.save()
            self.increase_news_quantity(request)
            if len(tags):
                self.tags_handler(tags=tags, news=news)
            return HttpResponseRedirect(reverse('news_details', kwargs={'pk': news.id}))

        news = NewsForm()
        return render(request, 'news/create_news.html', {'news': news})

    def tags_handler(self, tags, news):
        """
        На вход принимает tags (type str, пришли из формы create_news.html) и news (type obj News).
        Раздялеят строку на отдельные теги. Проверяет существуют ли теги в БД. Если нет, то сохраняет их в БД.
        Добавляет теги к новости.
        """
        tags_list = tags.split()
        tags_in_db = Tag.objects.all()
        tags_in_db_list = [str(tag) for tag in Tag.objects.all()]
        print(tags_in_db_list)
        if not tags_in_db.exists():
            for tag in tags_list:
                new_tag = Tag(name=tag)
                new_tag.save()
                news.tags.add(new_tag)
        else:
            for tag in tags_list:
                if tag in tags_in_db_list:
                    tag_for_add = tags_in_db.get(name=tag)
                    news.tags.add(tag_for_add)
                else:
                    new_tag = Tag(name=tag)
                    new_tag.save()
                    news.tags.add(new_tag)

    def increase_news_quantity(self, request):
        """
        Увеличивает на 1 количество новостей, созданных пользователем (атрибут written_news_quantity из Profile).
        """
        user = User.objects.get(username=request.user)
        user.profile.written_news_quantity += 1
        user.profile.save()
