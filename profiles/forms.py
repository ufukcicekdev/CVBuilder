from django import forms
from .models import Profile,Education,Experience,Skill,Certificate,CoverLetter,Project,SelfIntroduction
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import URLValidator


class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = Profile
        fields = ['full_name','job_title','contact_email', 'phone_number', 'address', 'profile_picture',
                  'github_link', 'facebook_link', 'linkedin_link', 'personal_website']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control'}),
            'personal_website': forms.URLInput(attrs={'class': 'form-control'}),
        }


    def clean_github_link(self):
        github_link = self.cleaned_data.get('github_link')
        if github_link:
            validate = URLValidator()
            try:
                validate(github_link)
                if 'github.com' not in github_link:
                    raise ValidationError("Please enter a valid GitHub profile link.")
            except ValidationError:
                raise ValidationError("Invalid GitHub profile link format.")
        return github_link

    def clean_facebook_link(self):
        facebook_link = self.cleaned_data.get('facebook_link')
        if facebook_link:
            validate = URLValidator()
            try:
                validate(facebook_link)
                if 'facebook.com' not in facebook_link:
                    raise ValidationError("Please enter a valid Facebook profile link.")
            except ValidationError:
                raise ValidationError("Invalid Facebook profile link format.")
        return facebook_link

    def clean_linkedin_link(self):
        linkedin_link = self.cleaned_data.get('linkedin_link')
        if linkedin_link:
            validate = URLValidator()
            try:
                validate(linkedin_link)
                if 'linkedin.com' not in linkedin_link:
                    raise ValidationError("Please enter a valid LinkedIn profile link.")
            except ValidationError:
                raise ValidationError("Invalid LinkedIn profile link format.")
        return linkedin_link



    

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Field of Study'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'End Date', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
        labels = {
            'institution': 'Institution',
            'degree': 'Degree',
            'field_of_study': 'Field of Study',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'description': 'Description',
        }
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date:
            if start_date > date.today():
                raise forms.ValidationError(
                    _("Start date cannot be in the future.")
                )

        if end_date and start_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    _("End date should be greater than or equal to start date.")
                )

        return cleaned_data
    



class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'End Date', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date:
            if start_date > date.today():
                raise forms.ValidationError(
                    _("Start date cannot be in the future.")
                )

        if end_date and start_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    _("End date should be greater than or equal to start date.")
                )

        return cleaned_data
    


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill Name'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rating (0-100)', 'max': 100, 'min': 0}),
        }
        labels = {
            'name': 'Skill Name',
            'description': 'Description',
            'rating': 'Rating',
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificate Name'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issuing Organization'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Issue Date', 'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Expiration Date', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('issue_date')
        end_date = cleaned_data.get('expiration_date')

        if start_date:
            if start_date > date.today():
                raise forms.ValidationError(
                    _("Start date cannot be in the future.")
                )

        if end_date and start_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    _("End date should be greater than or equal to start date.")
                )

        return cleaned_data
    


class CoverLetterForm(forms.ModelForm):
    class Meta:
        model = CoverLetter
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date:
            if start_date > date.today():
                raise forms.ValidationError(
                    _("Start date cannot be in the future.")
                )

        if end_date and start_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    _("End date should be greater than or equal to start date.")
                )

        return cleaned_data
    


class SelfIntroductionForm(forms.ModelForm):
    class Meta:
        model = SelfIntroduction
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            # Maximum file size allowed (50 MB)
            max_size = 50 * 1024 * 1024  # 50 MB in bytes
            if video.size > max_size:
                raise forms.ValidationError('The file size must be under 50 MB.')
        return video