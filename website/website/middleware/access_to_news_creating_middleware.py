from django.shortcuts import redirect

CREATE_NEWS_ADDRESS = '/interfax/create_news/'
REDIRECT_URL = '/interfax/'


class AccessNewsCreationMiddleware:
    """
    При побращении к странице CREATE_NEWS_ADDRESS проверяет есть ли у ползователя разрешение на создание новостей.
    Если нет, то перенаправляет пользователя на REDIRECT_URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if CREATE_NEWS_ADDRESS in request.path:
            if self.check_user_verification_status(request):
                return response
            return redirect(REDIRECT_URL)
        return response

    def check_user_verification_status(self, request):
        if request.user.is_authenticated:
            if not request.user.has_perm('news.add_news'):
                return False
            return True
