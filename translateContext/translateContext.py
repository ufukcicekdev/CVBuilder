from language.utils import get_translation
from django.utils import translation
from django.conf import settings





def get_trans_lang(request):
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
