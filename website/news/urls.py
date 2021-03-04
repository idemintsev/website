from django.urls import path

from news.views import (
    register_user, NewsListView, NewsDetailsView, Logout, AuthView, UserProfileView, NewsCreateFormView,
)

urlpatterns = [
    path('', NewsListView.as_view(), name='main'),
    path('interfax/', NewsListView.as_view(), name='interfax'),
    path('interfax/<int:pk>/', NewsDetailsView.as_view(), name='news_details'),
    path('interfax/create_news/', NewsCreateFormView.as_view(), name='create_news'),
    path('registration/', register_user, name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', AuthView.as_view(), name='login'),
    path('interfax/profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('interfax/news_list_by_tag/', NewsListView.as_view(), name='news_list_by_tag'),
]
