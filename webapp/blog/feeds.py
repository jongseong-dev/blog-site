from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from markdown import markdown

from blog.models import Post


class LatestPostsFeed(Feed):
    title = "My blog"
    # reverse 함수의 지연 버전
    # 프로젝트의 URL 구성이 로드되기 전에 URL을 사용할 수 있게 함
    # import 부터 evaluate 되기 때문에 reverse_lazy를 사용
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self):
        """
        Feed 에서 표시할 항목을 반환
        :return:
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
