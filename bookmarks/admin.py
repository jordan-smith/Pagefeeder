from django.contrib import admin
from bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'mark_date', 'push_date')
    list_filter = ['mark_date', 'push_date']
    search_fields = ['name', 'url']

admin.site.register(Bookmark, BookmarkAdmin)
