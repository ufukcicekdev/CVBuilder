from language.utils import get_translation,get_translation2
from django.utils import translation
from django.conf import settings
from profiles.models import Profile




def get_trans_lang(request):

    if request.user.is_authenticated:
        try:
            current_language = request.user.profile.language
        except Profile.DoesNotExist:
            pass  
    else:
        current_language = request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
    translation_dict1 = get_translation('header-footer', request)
    translation_dict2 = get_translation('signin-login-form', request)
    translation_dict3 = get_translation('mailtag', request)
    translation_dict4 = get_translation('messages', request)
    maincontext = {}
    maincontext.update(translation_dict1)
    maincontext.update(translation_dict2)
    maincontext.update(translation_dict3)
    maincontext.update(translation_dict4)
    maincontext['current_language'] = current_language
    return maincontext




def get_trans_lang_1(lang_code):
    translation_dict1 = get_translation2(lang_code, 'header-footer')
    translation_dict2 = get_translation2(lang_code, 'signin-login-form')
    translation_dict3 = get_translation2(lang_code, 'mailtag')
    translation_dict4 = get_translation2(lang_code, 'messages')
    maincontext = {}
    maincontext.update(translation_dict1)
    maincontext.update(translation_dict2)
    maincontext.update(translation_dict3)
    maincontext.update(translation_dict4)
    return maincontext
