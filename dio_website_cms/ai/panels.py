from django.template.loader import render_to_string
from wagtail.admin.panels import Panel


class FileLinkPanel(Panel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class BoundPanel(Panel.BoundPanel):
        def render_html(self, parent_context):  # noqa: ARG002
            instance = self.instance
            if instance.file:
                context = {
                    "file_url": instance.file.url,
                    "file_name": instance.file.name.split("/")[-1],
                }
                return render_to_string("upload/file.html", context)
            return "— Нет файла —"
