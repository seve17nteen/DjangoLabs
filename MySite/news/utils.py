from django.core.cache import cache
from .models import News


class MyMixin:
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()


class PopularNewsMixin:
    """Миксин для получения топ-10 популярных новостей с кэшированием"""

    def get_popular_news(self):
        popular = cache.get('top_10_popular_news')

        if popular is None:
            popular = list(News.objects.filter(is_published=True).order_by('-views')[:10])
            cache.set('top_10_popular_news', popular, 300)

        return popular


class ActiveLinkMixin:
    """Миксин для определения активной ссылки в навигации"""

    def get_active_link(self, request, link_name):
        if request.resolver_match.url_name == link_name:
            return 'active'
        return ''