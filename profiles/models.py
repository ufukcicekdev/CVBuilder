from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
# Create your models here.




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255,blank=True, null=True)
    contact_email = models.EmailField()
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True, verbose_name='GitHub Link')
    facebook_link = models.URLField(blank=True, null=True, verbose_name='Facebook Link')
    linkedin_link = models.URLField(blank=True, null=True, verbose_name='LinkedIn Link')
    personal_website = models.URLField(blank=True, null=True, verbose_name='Personal Website')

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('tr', 'Türkçe'),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return self.full_name
    

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)  # `null=True` ve `blank=True` ekleyin
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"
    


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=0, help_text="Enter a rating from 0 to 100.")

    def __str__(self):
        return self.name
    

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='certificates/images/', null=True, blank=True)

    def __str__(self):
        return self.name
    


class CoverLetter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cover Letter for {self.user.username}"
    


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class SelfIntroduction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='self_introductions/videos/', max_length=100, null=True, blank=True, help_text='Upload a video introducing yourself (max. 50MB)')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Self Introduction - {self.user.username}"
    

    @property
    def video_url(self):
        if self.video and hasattr(self.video, 'url'):
            return self.video.url
        return ''
    

class GeneratedCV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    html_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV for {self.user.username}"