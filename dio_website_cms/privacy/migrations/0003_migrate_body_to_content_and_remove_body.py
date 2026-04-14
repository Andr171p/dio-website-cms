import copy

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
from django.db import migrations
from django.utils.html import escape


def _normalize_stream_data(stream_data):
    normalized = []

    for block in stream_data or []:
        block_type = block.get("type")
        block_value = block.get("value")

        if block_type == "table" and isinstance(block_value, dict) and "table" in block_value:
            title = (block_value.get("title") or "").strip()
            table_value = block_value.get("table")

            if title:
                normalized.append(
                    {
                        "type": "text",
                        "value": f"<h2>{escape(title)}</h2>",
                    }
                )

            normalized.append(
                {
                    "type": "table",
                    "value": table_value,
                }
            )
            continue

        normalized.append(copy.deepcopy(block))

    return normalized


def migrate_privacy_content(apps, schema_editor):
    PrivacyPolicyPage = apps.get_model("privacy", "PrivacyPolicyPage")

    for page in PrivacyPolicyPage.objects.all():
        content = getattr(page, "content", None)
        stream_data = copy.deepcopy(getattr(content, "raw_data", content) or [])
        body = (getattr(page, "body", "") or "").strip()

        if stream_data:
            normalized = _normalize_stream_data(stream_data)
            if normalized != stream_data:
                page.content = normalized
                page.save(update_fields=["content"])
            continue

        if body:
            page.content = [
                {
                    "type": "text",
                    "value": body,
                }
            ]
            page.save(update_fields=["content"])


class Migration(migrations.Migration):

    dependencies = [
        ("privacy", "0002_privacypolicypage_content_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_privacy_content, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="privacypolicypage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    (
                        "text",
                        wagtail.blocks.RichTextBlock(
                            features=["h2", "h3", "h4", "bold", "italic", "link", "ol", "ul"],
                            label="Text",
                        ),
                    ),
                    (
                        "table",
                        wagtail.contrib.table_block.blocks.TableBlock(label="Table"),
                    ),
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Page content",
            ),
        ),
        migrations.RemoveField(
            model_name="privacypolicypage",
            name="body",
        ),
    ]
