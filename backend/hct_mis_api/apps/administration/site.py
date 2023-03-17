from typing import Any, List

from django.core.cache import caches, cache as dj_cache
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.conf import settings
from django.contrib import messages
from django.contrib.messages import add_message

from hct_mis_api.apps.administration.forms import ClearCacheForm

from constance import config
from smart_admin.site import SmartAdminSite

cache = caches["default"]


def clean(v: str) -> str:
    return v.replace(r"\n", "").strip()


def get_bookmarks(request: Any) -> List:
    quick_links = []
    for entry in config.QUICK_LINKS.split("\n"):
        if entry := clean(entry):
            try:
                if entry == "--":
                    quick_links.append(mark_safe("<li><hr/></li>"))
                elif parts := entry.split(","):
                    args = None
                    if len(parts) == 1:
                        args = parts[0], "viewlink", parts[0], parts[0]
                    elif len(parts) == 2:
                        args = parts[0], "viewlink", parts[1], parts[0]
                    elif len(parts) == 3:
                        args = parts[0], "viewlink", parts[1], parts[0]
                    elif len(parts) == 4:
                        parts.reverse()
                    if args:
                        quick_links.append(format_html('<li><a target="{}" class="{}" href="{}">{}</a></li>', *args))
            except ValueError:
                pass
    return quick_links


# admin view
def clean_cache_view(request: "HttpRequest") -> "HttpResponse":
    template = "admin/clean_cache.html"
    ctx = {
        "title": "Clean Cache",
        "cache_keys": [],
        "is_root": False,
        "form": ClearCacheForm(),
    }

    if not getattr(settings, "IS_TEST", False):
        # skip name started with numbers
        ctx["cache_keys"] = [key for key in dj_cache.keys("*") if key[0].isalpha()]

        if request.user.is_superuser:
            ctx["is_root"] = True
            if request.POST:
                form = ClearCacheForm(request.POST)
                if form.is_valid():
                    selected_keys = [k for k, v in form.cleaned_data.items() if v is True]
                    for k in [key for key in dj_cache.keys("*") if key.startswith(tuple(selected_keys))]:
                        dj_cache.delete(k)

                    ctx["cache_keys"] = [key for key in dj_cache.keys("*") if key[0].isalpha()]
                    add_message(request, messages.SUCCESS, f"Finished clean cache for: {selected_keys}")
            return render(request, template, ctx)
        else:
            add_message(request, messages.ERROR, "Access Not Allowed. Only superuser have access to clean cache")
            return render(request, template, ctx)
    else:
        add_message(request, messages.ERROR, "Not Possible Clean Cache For Test Settings")
        return render(request, template, ctx)


class HopeAdminSite(SmartAdminSite):
    site_title = "HOPE"
    site_header = "HOPE Administration"
    index_title = "Index"

    def get_urls(self) -> List:
        urls = super().get_urls()
        custom_urls = [
            path("clean-cache/", self.admin_view(clean_cache_view), name="clean_cache"),
        ]
        return custom_urls + urls


site = HopeAdminSite()
