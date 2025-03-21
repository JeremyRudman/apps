# Generated by Django 4.2.13 on 2025-01-11 22:26

import django.db.models.deletion
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0093_uploadedfile"),
        ("cms", "0002_cmspage"),
    ]

    operations = [
        migrations.CreateModel(
            name="CmsStreamPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "paragraph",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "alignment",
                                            wagtail.blocks.ChoiceBlock(
                                                choices=[
                                                    ("left", "Left"),
                                                    ("center", "Center"),
                                                    ("right", "Right"),
                                                ]
                                            ),
                                        ),
                                        ("paragraph", wagtail.blocks.RichTextBlock()),
                                    ],
                                    features=[
                                        "h2",
                                        "h3",
                                        "h4",
                                        "bold",
                                        "italic",
                                        "ol",
                                        "ul",
                                        "hr",
                                        "link",
                                        "document-link",
                                        "image",
                                        "embed",
                                        "code",
                                        "blockquote",
                                    ],
                                ),
                            ),
                            ("html", wagtail.blocks.RawHTMLBlock()),
                            (
                                "table",
                                wagtail.contrib.table_block.blocks.TableBlock(
                                    table_options={
                                        "contextMenu": [
                                            "row_above",
                                            "row_below",
                                            "---------",
                                            "col_left",
                                            "col_right",
                                            "---------",
                                            "remove_row",
                                            "remove_col",
                                            "---------",
                                            "undo",
                                            "redo",
                                            "---------",
                                            "copy",
                                            "cut",
                                            "---------",
                                            "alignment",
                                        ]
                                    }
                                ),
                            ),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="NavigationContainerPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "verbose_name": "Navigation Container Page",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.DeleteModel(
            name="CmsPage",
        ),
    ]
