from django.template.loader import get_template
from .models import GeneratedCV, CoverLetter, SelfIntroduction, Education, Experience, Project, Skill, Certificate

def generate_or_update_cv(user):
    # Kullanıcının mevcut GeneratedCV kaydını al
    cv_generate = GeneratedCV.objects.filter(user=user).first()

    # Kullanıcının profil, eğitim, deneyim, sertifika, vb. bilgilerini topla
    cover_letter = CoverLetter.objects.filter(user=user).first()
    self_introduction = SelfIntroduction.objects.filter(user=user).first()

    user_data = {
            'full_name': user.profile.full_name,
            'job_title': user.profile.job_title,
            'contact_email': user.profile.contact_email,
            'phone_number': user.profile.phone_number,
            'address': user.profile.address,
            'profile_picture': user.profile.profile_picture.url if user.profile.profile_picture else '',
            'github_link': user.profile.github_link,
            'linkedin_link': user.profile.linkedin_link,
            'facebook_link': user.profile.facebook_link,
            'personal_website': user.profile.personal_website,
            'educations': Education.objects.filter(user=user),
            'experiences': Experience.objects.filter(user=user),
            'projects': Project.objects.filter(user=user),
            'skills':  Skill.objects.filter(user=user),
            'certificates':  Certificate.objects.filter(user=user),
            'cover_letter': cover_letter if cover_letter else "",
            'self_introduction': self_introduction if self_introduction else ""

        }

    # CV HTML şablonunu oluştur
    template = get_template('cvTemp/cv_template.html')
    html_content = template.render({'user_data': user_data})

    if cv_generate:
        # Eğer CV zaten varsa, güncelle
        cv_generate.html_content = html_content
        cv_generate.save()
    else:
        pass
from django.template.loader import get_template
from .models import GeneratedCV, CoverLetter, SelfIntroduction, Education, Experience, Project, Skill, Certificate

def generate_or_update_cv(user):
    # Kullanıcının mevcut GeneratedCV kaydını al
    cv_generate = GeneratedCV.objects.filter(user=user).first()

    # Kullanıcının profil, eğitim, deneyim, sertifika, vb. bilgilerini topla
    cover_letter = CoverLetter.objects.filter(user=user).first()
    self_introduction = SelfIntroduction.objects.filter(user=user).first()

    user_data = {
            'full_name': user.profile.full_name,
            'job_title': user.profile.job_title,
            'contact_email': user.profile.contact_email,
            'phone_number': user.profile.phone_number,
            'address': user.profile.address,
            'profile_picture': user.profile.profile_picture.url if user.profile.profile_picture else '',
            'github_link': user.profile.github_link,
            'linkedin_link': user.profile.linkedin_link,
            'facebook_link': user.profile.facebook_link,
            'personal_website': user.profile.personal_website,
            'educations': Education.objects.filter(user=user),
            'experiences': Experience.objects.filter(user=user),
            'projects': Project.objects.filter(user=user),
            'skills':  Skill.objects.filter(user=user),
            'certificates':  Certificate.objects.filter(user=user),
            'cover_letter': cover_letter if cover_letter else "",
            'self_introduction': self_introduction if self_introduction else ""

        }

    # CV HTML şablonunu oluştur
    template = get_template('cvTemp/cv_template.html')
    html_content = template.render({'user_data': user_data})

    if cv_generate:
        # Eğer CV zaten varsa, güncelle
        cv_generate.html_content = html_content
        cv_generate.save()
    else:
        pass
