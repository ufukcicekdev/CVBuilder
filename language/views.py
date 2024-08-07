from django.shortcuts import redirect
from django.utils import translation
from cv_builder.settings import *
from profiles.models import Profile


def set_language(request):
    language_code = request.GET.get('language', 'en')
    translation.activate(language_code)
    request.session[LANGUAGE_COOKIE_NAME] = language_code

    # Kullanıcının profilindeki dil tercihini güncelle
    if request.user.is_authenticated:
        try:
            # Profil mevcutsa güncelle
            profile = request.user.profile
            profile.language = language_code
            profile.save()
        except Profile.DoesNotExist:
            # Profil mevcut değilse, yeni bir profil oluştur veya uygun bir işlem yap
            Profile.objects.create(user=request.user, language=language_code)

    return redirect(request.GET.get('next', '/'))

