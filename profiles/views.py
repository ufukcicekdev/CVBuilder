from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from translateContext.translateContext import get_trans_lang
from .models import Profile,Education,Experience,Skill,Certificate,Project,SelfIntroduction,GeneratedCV
from .forms import ProfileForm,EducationForm,ExperienceForm,SkillForm,CertificateForm,CoverLetterForm,CoverLetter,ProjectForm,SelfIntroductionForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import JsonResponse



@login_required(login_url='accounts:signin')
def profile(request):
    mainContext = get_trans_lang(request)
    # Kullanıcının profili
    profile = Profile.objects.filter(user=request.user).first()
    educations = Education.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    certificates = Certificate.objects.filter(user=request.user)
    cover_letters =CoverLetter.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    self_introduction = SelfIntroduction.objects.filter(user=request.user).first()
    cv_generation_id = GeneratedCV.objects.filter(user=request.user).first()


    context = {
        'profile': profile, 
        'educations': educations,
        'experiences':experiences,
        'skills':skills,
        'certificates':certificates,
        'cover_letters':cover_letters,
        'projects':projects,
        'self_introduction':self_introduction,
        'cv_generation_id':cv_generation_id
    }
    
    mainContext.update(context)

    return render(request, 'profiles/profile.html', mainContext)


@login_required(login_url='accounts:signin')
def generate_cv(request):
    cv_generate = GeneratedCV.objects.filter(user=request.user).first()
    if cv_generate:
        return redirect('profile:view_cv', cv_generate.id)
    else:
        user = request.user
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

        # CV HTML şablonunu oluşturalım
        template = get_template('cvTemp/cv_template.html')
        html_content = template.render({'user_data': user_data})

        # Veritabanına kaydet
        generated_cv = GeneratedCV(user=user, html_content=html_content)
        generated_cv.save()

        cv_generate = GeneratedCV.objects.filter(user=request.user).first()

        return redirect('profile:view_cv', cv_generate.id)


def view_cv(request, cv_id):
    try:
        generated_cv = GeneratedCV.objects.get(id=cv_id)
        return HttpResponse(generated_cv.html_content)
    except GeneratedCV.DoesNotExist:
        return HttpResponse("CV not found")



@login_required(login_url='accounts:signin')
def delete_cv(request, pk):
    cv = get_object_or_404(GeneratedCV, pk=pk)
    if request.method == 'POST':
        cv.delete()
        messages.success(request, 'CV deleted successfully.')
        return redirect('profile:profile')
    return redirect('profile:profile')



@login_required(login_url='accounts:signin')
def edit_profile_view(request):
    mainContext = get_trans_lang(request)
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_profile.html', mainContext)



@login_required(login_url='accounts:signin')
def add_education(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, 'Education information added successfully!')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EducationForm()
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_education.html', mainContext)

@login_required(login_url='accounts:signin')
def edit_education(request, education_id):
    mainContext = get_trans_lang(request)
    education = get_object_or_404(Education, id=education_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            education = form.save(commit=False)
            if form.cleaned_data['end_date'] is None:
                education.end_date = None
            education.save()
            messages.success(request, 'Education information updated successfully!')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EducationForm(instance=education)
    context = {
        'form':form,
        'education': education
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_education.html', mainContext)

@login_required(login_url='accounts:signin')
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Education information deleted successfully.')
        return redirect('profile:profile')  # veya başka bir sayfaya yönlendirme yapabilirsiniz
    
    messages.error(request, 'Invalid request. Please use the delete button to delete education information.')
    return redirect('profile:profile')  




@login_required(login_url='accounts:signin')
def add_experience(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user  # Eğer kullanıcıya bağlı bir deneyim eklemesi yapılacaksa
            experience.save()
            messages.success(request, 'Experience added successfully!')
            return redirect('profile:profile')  # Başka bir sayfaya yönlendirilebilir
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExperienceForm()

    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_experience.html', mainContext)

@login_required(login_url='accounts:signin')
def edit_experience(request, pk):
    mainContext = get_trans_lang(request)
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated successfully!')
            return redirect('profile:profile')  # Başka bir sayfaya yönlendirilebilir
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExperienceForm(instance=experience)

    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_experience.html', mainContext)

@login_required(login_url='accounts:signin')
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Experience deleted successfully!')
        return redirect('profile:profile')  # Başka bir sayfaya yönlendirilebilir
    # Silme işlemi onaylanmadığında veya başka bir durumda farklı bir işlem yapılabilir
    messages.error(request, 'Invalid request. Please use the delete button to delete experience information.')
    return render(request, 'profiles/confirm_experience_delete.html', {'experience': experience})





@login_required(login_url='accounts:signin')
def add_skill(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('profile:profile')  # veya başka bir sayfaya yönlendirme yapılabilir
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SkillForm()
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_skill.html', mainContext)



@login_required(login_url='accounts:signin')
def edit_skill(request, pk):
    mainContext = get_trans_lang(request)
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('profile:profile')  # veya başka bir sayfaya yönlendirme yapılabilir
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SkillForm(instance=skill)
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_skill.html', {'form': form})


@login_required(login_url='accounts:signin')
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('profile:profile')  # veya başka bir sayfaya yönlendirme yapılabilir
    
    messages.error(request, 'Invalid request. Please use the delete button to delete skill information.')
    return render(request, 'profiles/delete_skill.html', {'skill': skill})




@login_required(login_url='accounts:signin')
def add_certificate(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = CertificateForm(request.POST ,request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = request.user
            certificate.save()
            messages.success(request, 'Certificate added successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CertificateForm()

    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_certificate.html', mainContext)


@login_required(login_url='accounts:signin')
def edit_certificate(request, pk):
    mainContext = get_trans_lang(request)
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate updated successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CertificateForm(instance=certificate)
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_certificate.html', mainContext)

@login_required(login_url='accounts:signin')
def delete_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        certificate.delete()
        messages.success(request, 'Certificate deleted successfully.')
        return redirect('profile:profile')
    messages.error(request, 'Invalid request. Please use the delete button to delete certificate information.')
    return render(request, 'profiles/delete_certificate.html', {'certificate': certificate})





@login_required(login_url='accounts:signin')
def add_cover_letter(request):
    mainContext = get_trans_lang(request)
    existing_cover_letter = CoverLetter.objects.filter(user=request.user).first()

    if existing_cover_letter:
        messages.warning(request, 'You can only have one cover letter. Please edit your existing cover letter.')
        return redirect('profile:profile')
    
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            cover_letter = form.save(commit=False)
            cover_letter.user = request.user
            cover_letter.save()
            messages.success(request, 'Cover letter added successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CoverLetterForm()
    
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_cover_letter.html', mainContext)


@login_required(login_url='accounts:signin')
def edit_cover_letter(request,pk):
    mainContext = get_trans_lang(request)
    cover_letter = get_object_or_404(CoverLetter, pk=pk)
    if request.method == 'POST':
        form = CoverLetterForm(request.POST, instance=cover_letter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cover letter updated successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CoverLetterForm(instance=cover_letter)
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_cover_letter.html', mainContext)


@login_required(login_url='accounts:signin')
def delete_cover_letter(request, pk):
    cover_letter = get_object_or_404(CoverLetter, pk=pk)
    if request.method == 'POST':
        cover_letter.delete()
        messages.success(request, 'Cover letter deleted successfully.')
        return redirect('profile:profile')
    messages.error(request, 'Invalid request. Please use the delete button to delete cover letter information.')
    return redirect('profile:profile')







@login_required(login_url='accounts:signin')
def add_project(request):
    mainContext = get_trans_lang(request)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project added successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    context = {
        'form':form
    }
    mainContext.update(context)
    return render(request, 'profiles/add_project.html', mainContext)





@login_required(login_url='accounts:signin')
def edit_project(request, pk):
    mainContext = get_trans_lang(request)
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
    context = {
        'form':form,
        'project': project
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_project.html', mainContext)



@login_required(login_url='accounts:signin')
def edit_project(request, pk):
    mainContext = get_trans_lang(request)
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
    context = {
        'form':form,
        'project': project
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_project.html', mainContext)


@login_required(login_url='accounts:signin')
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('profile:profile')
    
    messages.error(request, 'Invalid request. Please use the delete button to delete project information.')
    return redirect('profile:profile')







@login_required(login_url='accounts:signin')
def add_self_introduction(request):
    mainContext = get_trans_lang(request)
    self_introduction = SelfIntroduction.objects.filter(user=request.user).first()

    if self_introduction:
        messages.warning(request, 'You already have a self-introduction video. Please edit your existing introduction.')
        return redirect('profile:profile')


    if request.method == 'POST':
        form = SelfIntroductionForm(request.POST, request.FILES)
        if form.is_valid():
            self_introduction = form.save(commit=False)
            self_introduction.user = request.user  # Assuming user is logged in
            self_introduction.save()
            messages.success(request, 'Self introduction video uploaded successfully.')
            return redirect('profile:profile')  # Redirect to profile page or wherever needed
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SelfIntroductionForm()

    context = {
        'form':form,
    }
    mainContext.update(context)
    
    return render(request, 'profiles/add_self_introduction.html', mainContext)



@login_required(login_url='accounts:signin')
def edit_self_introduction(request, pk):
    mainContext = get_trans_lang(request)
    self_introduction = SelfIntroduction.objects.filter(pk=pk).first()  # Assuming there's only one self introduction per user
    if request.method == 'POST':
        form = SelfIntroductionForm(request.POST, request.FILES, instance=self_introduction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Self introduction video updated successfully.')
            return redirect('profile:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SelfIntroductionForm(instance=self_introduction)
    context = {
        'form':form,
    }
    mainContext.update(context)
    return render(request, 'profiles/edit_self_introduction.html', mainContext)

@login_required(login_url='accounts:signin')
def delete_self_introduction(request, pk):
    self_introduction = get_object_or_404(SelfIntroduction, pk=pk)
    if request.method == 'POST':
        self_introduction.delete()
        messages.success(request, 'Self introduction video deleted successfully.')
        return redirect('profile:profile')
    return render(request, 'delete_self_introduction.html', {'self_introduction': self_introduction})

