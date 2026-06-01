from .models import News
class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()
    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
         return s.title.upper()


class PopularNewsMixin:
    """Миксин для получения топ-5 популярных новостей"""

    def get_popular_news(self):
        return News.objects.filter(is_published=True).order_by('-views')[:5]


class ActiveLinkMixin:
    """Миксин для определения активной ссылки в навигации"""

    def get_active_link(self, request, link_name):
        """Возвращает 'active', если текущий URL соответствует имени ссылки"""
        if request.resolver_match.url_name == link_name:
            return 'active'
        return ''