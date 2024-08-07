from django.conf import settings
from .models import Translation, Language, LanguageTag
from cv_builder.settings import *
from profiles.models import Profile


def get_translation(tag_name, request):
    language_code = settings.LANGUAGE_CODE

    if request.user.is_authenticated:
        try:
            language_code = request.user.profile.language
        except Profile.DoesNotExist:
            pass  

    else:
        language_code = request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)

    try:
        language = Language.objects.get(code=language_code)
        tag = LanguageTag.objects.get(name=tag_name)
        translations = Translation.objects.filter(language=language, tag=tag)
        
        translation_dict = {translation.key: translation.text for translation in translations}
        
        return translation_dict
    except (Language.DoesNotExist, LanguageTag.DoesNotExist, Translation.DoesNotExist):
        return {} 
    

def get_translation2(lang_code, tag_name):
    try:
        language = Language.objects.get(code=lang_code)
        tag = LanguageTag.objects.get(name=tag_name)
        translations = Translation.objects.filter(language=language, tag=tag)
        
        translation_dict = {translation.key: translation.text for translation in translations}
        
        return translation_dict
    except (Language.DoesNotExist, LanguageTag.DoesNotExist, Translation.DoesNotExist):
        return {} 