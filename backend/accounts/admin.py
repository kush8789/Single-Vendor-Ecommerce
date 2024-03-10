from django.contrib import admin

# Register your models here.

admin.site.site_header = "Admin Panel"
admin.site.index_title = "Welcome to the admin panel"

admin.site.site_title = "Accounts"

class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username', 'email')