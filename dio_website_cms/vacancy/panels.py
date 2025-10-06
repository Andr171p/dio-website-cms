from django.template.loader import render_to_string
from wagtail.admin.panels import Panel


class ResumeLinkPanel(Panel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class BoundPanel(Panel.BoundPanel):
        def render_html(self, parent_context):  # noqa: ARG002
            instance = self.instance
            if instance.resume_link != "Нет резюме":
                context = {"resume_link": instance.resume_link or None}
                return render_to_string("vacancy/resume_link_panel.html", context)
            return "Нету резюме"
