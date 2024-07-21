from django.conf import settings
from .models import Translation, Language, LanguageTag
from cv_builder.settings import *



def get_translation(tag_name, request):
    language_code = request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
    try:
        language = Language.objects.get(code=language_code)
        tag = LanguageTag.objects.get(name=tag_name)
        translations = Translation.objects.filter(language=language, tag=tag)
        
        translation_dict = {translation.key: translation.text for translation in translations}
        
        return translation_dict
    except (Language.DoesNotExist, LanguageTag.DoesNotExist, Translation.DoesNotExist):
        return {} 
