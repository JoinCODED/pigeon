from django.contrib import admin
from main.models import Group,Recipient
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import AdminSite
from main import views
from django.urls import path
from django.shortcuts import  redirect
from django.utils.html import format_html
from django.urls import reverse

def distributor(modeladmin, request, queryset):
    
    query = queryset.first().id
    return redirect('admin:distributor', query=query)
distributor.short_description = "Select one group to send messages"

class RecipientResources(resources.ModelResource):
    class Meta:
        model = Recipient
        skip_unchanged = True
        report_skipped = True

class MembershipInline(admin.TabularInline):
    model = Group.members.through
    raw_id_fields = ('recipient',)
    search_fields = ('recipient__name',)
    
class RecipientAdmin(ImportExportModelAdmin):
    resource_class = RecipientResources
    search_fields = ('name','email','number')

class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    actions = [distributor]
    inlines = [
        
        MembershipInline
    ]
    list_per_page = 20
    exclude = ('members',)
    list_display = (
        'name',
        'counter',
        'group_actions', 
    )
    def group_actions(self, obj):
        return format_html('<a class="button" href="{}">Distributor</a>&nbsp;''<a class="button" href="{}">Quick Add/Delete</a>&nbsp;',reverse('admin:distributor', args=[obj.id]),reverse('admin:recipientsList', args=[obj.id]))

class MyAdminSite(AdminSite):
    site_header = 'Pigeon Headquarters'
    

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()
        custom_urls = [
            path('recipients/groups/<int:query>', self.admin_view(views.recipientsList), name="recipientsList"),
            path('groups/distributor/<int:query>', self.admin_view(views.distributor), name="distributor"),

        ]
        return urls + custom_urls



admin_site = MyAdminSite(name='admin')
admin_site.register(Recipient,RecipientAdmin)
admin_site.register(Group, GroupAdmin)
