from django.conf import settings
from django.contrib import admin

from admin_extra_urls.decorators import button
from admin_extra_urls.mixins import ExtraUrlMixin, _confirm_action
from smart_admin.mixins import DisplayAllMixin as SmartDisplayAllMixin


def is_root(request, obj):
    return request.user.is_superuser and request.headers.get("x-root-token") == settings.ROOT_TOKEN


class SoftDeletableAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_list_filter(self, request):
        return super().get_list_filter(request) + ("is_removed",)


class HOPEModelAdminBase(SmartDisplayAllMixin, admin.ModelAdmin):
    list_per_page = 50

    def get_fields(self, request, obj=None):
        return super().get_fields(request, obj)

    # def get_common_context(self, request, pk=None, **kwargs):
    #     opts = self.model._meta
    #     app_label = opts.app_label
    #     self.object = None
    #
    #     context = {
    #         **self.admin_site.each_context(request),
    #         **kwargs,
    #         "opts": opts,
    #         "app_label": app_label,
    #     }
    #     if pk:
    #         self.object = self.get_object(request, pk)
    #         context["original"] = self.object
    #     return context


class LastSyncDateResetMixin(ExtraUrlMixin):
    @button()
    def reset_sync_date(self, request):
        if request.method == "POST":
            self.get_queryset(request).update(last_sync_at=None)
        else:
            return _confirm_action(
                self,
                request,
                self.reset_sync_date,
                "Continuing will reset all records last_sync_date field.",
                "Successfully executed",
                title="aaaaa",
            )

    @button(label="reset sync date")
    def reset_sync_date_single(self, request, pk):
        if request.method == "POST":
            self.get_queryset(request).filter(id=pk).update(last_sync_at=None)
        else:
            return _confirm_action(
                self,
                request,
                self.reset_sync_date,
                "Continuing will reset last_sync_date field.",
                "Successfully executed",
            )
