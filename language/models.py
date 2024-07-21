from django.db import models
from django.utils.translation import gettext_lazy as _

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Language Code"))
    name = models.CharField(max_length=100, verbose_name=_("Language Name"))

    def __str__(self):
        return self.name
    

class LanguageTag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Language Name"))

    def __str__(self):
        return self.name

class Translation(models.Model):
    key = models.CharField(max_length=255, verbose_name=_("Key"))
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_("Language"))
    text = models.TextField(verbose_name=_("Text"))
    tag = models.ForeignKey(LanguageTag, on_delete=models.CASCADE, verbose_name=_("Language Tag"), blank=True, null=True)


    class Meta:
        unique_together = ('key', 'language')

    def __str__(self):
        return f"{self.key} ({self.language.code})"
