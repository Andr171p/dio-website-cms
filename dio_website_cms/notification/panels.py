from django.template.loader import render_to_string
from wagtail.admin.panels import Panel


class URLPanel(Panel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class BoundPanel(Panel.BoundPanel):
        def render_html(self, parent_context):  # noqa: ARG002
            instance = self.instance
            context = {"url": instance.url or None}
            return render_to_string("notifications/link.html", context)
