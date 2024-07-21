from django.contrib import admin
from .models import Language, Translation, LanguageTag


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', 'code')

@admin.register(LanguageTag)
class LanguageTagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('key', 'language', 'text', "tag")
    list_filter = ('language',)
    search_fields = ('key', 'text',"tag")
