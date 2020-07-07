from django.urls import reverse
from django.utils.html import format_html


def linkify(field_name):
    """
    Converts a foreign key value into clickable links

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        try:
            app_label = obj._meta.app_label
            linked_obj = getattr(obj, field_name)
            model_name = linked_obj._meta.model_name
            view_name = f"admin:{app_label}_{model_name}_change"
            link_url = reverse(view_name, args=[linked_obj.pk])
            return format_html('<a href="{}">{}</a>', link_url, linked_obj)
        except AttributeError:
            return None

    _linkify.short_description = field_name  # Sets column name
    return _linkify