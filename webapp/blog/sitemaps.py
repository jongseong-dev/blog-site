from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSiteMap(Sitemap):
    # changefreq, priority는 게시물 페이지의 변경 빈도와 사이트에서의 관련성을 나타냄
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        """
        사이트맵에 포함할 객체들의 QuerySet을 반환
        기본적으로 장고는 각 객체에서 get_absolute_url() 메서드를 호출하여 URL을 조회한다.
        각 객체에 URL을 지정하려는 경우 사이트맵 클래스에 location 메서드를 추가할 수 있다.
        :return:
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        items()에서 반환된 각 객체를 받아서 객체가 마지막으로 수정된 시간을 반환한다.
        :param obj:
        :return:
        """
        return obj.updated_at
