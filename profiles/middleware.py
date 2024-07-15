from django.utils.deprecation import MiddlewareMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .utils import *




class UpdateCVMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            profile_updated = Profile.objects.filter(user=user).exists()
            education_updated = Education.objects.filter(user=user).exists()
            experience_updated = Experience.objects.filter(user=user).exists()
            skill_updated = Skill.objects.filter(user=user).exists()
            certificate_updated = Certificate.objects.filter(user=user).exists()
            cover_letter_updated = CoverLetter.objects.filter(user=user).exists()
            project_updated = Project.objects.filter(user=user).exists()
            self_introduction_updated = SelfIntroduction.objects.filter(user=user).exists()

            if (profile_updated or education_updated or experience_updated or
                skill_updated or certificate_updated or cover_letter_updated or
                project_updated or self_introduction_updated):
                generate_or_update_cv(user)