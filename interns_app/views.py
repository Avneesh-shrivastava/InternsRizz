from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')

def signup_view(request):
    # if request.user.is_authenticated:
    #         return redirect("profile_setup")

    if request.method == "POST":
            print('form submitted')
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            username = request.POST.get("username")


            # Check passwords
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("signup_view")

            # Check existing email
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect("signup_view")

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name
            )
            print('user created')

            # Log the user in
            login(request, user)
            print("account created")
            return redirect("profile_setup")

    return render(request, "signup.html")

def login_view(request):

    # if request.user.is_authenticated:
    #     return redirect("job_feed")

    if request.method == "POST":
        print('form submitted')
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)

        user = authenticate(
            request,
            username=username.strip(),
            password=password.strip()
        )
        print(user)

        if user is not None:

            login(request, user)
            print("logged_in")
            return redirect("job_feed")

        else:

            messages.error(
                request,
                "Invalid email or password."
            )

            return redirect("login_view")

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("login")

@login_required(login_url='/login-view/')
def profile_setup(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        preferred_role = request.POST.get("preferred_role")

        education = request.POST.get("education")
        college = request.POST.get("college")
        graduation_year = request.POST.get("graduation_year")
        experience = request.POST.get("experience")

        skills = request.POST.get("skills")
        
        about = request.POST.get("about")

        resume = request.FILES.get("resume")

        # Update user's name
        request.user.first_name = full_name
        request.user.save()

        # Create or update profile
        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        profile.phone = phone
        profile.location = location
        profile.preferred_role = preferred_role
        profile.education = education
        profile.college = college
        profile.graduation_year = graduation_year
        profile.experience = experience
        profile.skills = skills
        profile.about = about

        if resume:
            profile.resume = resume

        profile.save()

        return redirect("job_feed")

    return render(request, "profile_setup.html")

@login_required(login_url='/login-view/')
def job_feed(request):
    job_swipe_ids = JobSwipe.objects.filter(user=request.user).values_list('job_id', flat=True)

    curr_job_role = ""
    if request.method == "POST":
        curr_job_role = request.POST.get('preferred_role')
        return redirect(f"/job-feed/?role={curr_job_role}")

    curr_job_role = request.GET.get("role", "")
    if curr_job_role != "":
        jobs = Job.objects.filter(is_active=True,job_role=curr_job_role).exclude(id__in=job_swipe_ids)
    else:
        jobs = Job.objects.filter(is_active=True).exclude(id__in=job_swipe_ids)



    


    return render(request, "job_feed.html", {
        "jobs": jobs,
        "curr_job_role" : curr_job_role 
    })

def swipe_job(request):
    try:
        data = json.loads(request.body)
        job_id = data.get("job_id")
        decision = data.get("decision")

        if decision not in [
            "interested",
            "not_interested",
            "saved",
        ]:
            return JsonResponse(
                {"error": "Invalid decision."},
                status=400,
            )

        job = Job.objects.get(
            id=job_id,
            is_active=True,
        )

        swipe, created = JobSwipe.objects.update_or_create(
            user=request.user,
            job=job,
            defaults={"decision": decision},
        )

        return JsonResponse({
            "success": True,
            "decision": swipe.decision,
        })

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400,
        )

    except Job.DoesNotExist:
        return JsonResponse(
            {"error": "Job not found."},
            status=404,
        )


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )
    return render(request, "profile.html", {
        "profile": profile
    })

@login_required
def saved_jobs_view(request):
    saved_jobs = (
        JobSwipe.objects
        .filter(user=request.user, decision="saved", job__is_active=True)
        .select_related("job")
        .order_by("-updated_at")
    )

    return render(request, "saved_jobs.html", {
        "saved_jobs": saved_jobs
    })

@login_required
def interested_jobs(request):
    interested_jobs = JobSwipe.objects.filter(
            user=request.user,
            decision="interested",
            job__is_active=True
        ).select_related("job").order_by("-updated_at")

    if request.method == "POST":
            job_id = request.POST.get("job_id")

            JobSwipe.objects.filter(
                user=request.user,
                job_id=job_id,
                decision="interested"
            ).update(decision="not_interested")

            return redirect(request.path)

    return render(request, "interested_jobs.html", {
        "interested_jobs": interested_jobs
    })

@login_required
def interested_jobs_del(request, job_id):
    interested_job = JobSwipe.objects.get(id=job_id)
    interested_job.decision = 'saved'
    interested_job.save()
    return redirect("interested_jobs")



@login_required
def edit_profile(request):
    
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        
        profile.phone = request.POST.get("phone", "")
        profile.location = request.POST.get("location", "")
        profile.preferred_role = request.POST.get("preferred_role", "")
        profile.education = request.POST.get("education", "")
        profile.college = request.POST.get("college", "")
        profile.graduation_year = request.POST.get("graduation_year") or None
        profile.experience = request.POST.get("experience", "")
        profile.skills = request.POST.get("skills", "")
        profile.about = request.POST.get("about", "")

        if request.FILES.get("resume"):
            profile.resume = request.FILES["resume"]

        profile.save()
        print("profile created")

        return redirect("profile_view")

    return render(request, "edit_profile.html", {
        "profile": profile
    })

@login_required
def rec_dashboard(request):
    

    context = {
      
    }

    return render(request, 'rec_dashboard.html',context)


def rec_login(request):
    if request.method == "POST":
        
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )
  
        if user is not None:

            if RecruiterProfile.objects.filter(user=user).exists():

                login(request, user)
                return redirect("rec_dashboard")

            else:
                messages.error(
                    request,
                    "This account is not registered as a recruiter."
                )

        else:
            messages.error(request, "Invalid email or password.")
        return redirect('rec_login')
    return render(request, 'rec_login.html')

def rec_signup(request):
    
    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        print(email)
        company_name = request.POST.get("company", "").strip()
        designation = request.POST.get("designation", "").strip()
        password = request.POST.get("password", "")
        print(password)
        confirm_password = request.POST.get("confirm_password", "")

        if not all([username, email, company_name, designation,
                    password, confirm_password]):
            messages.error(request, "Please fill all fields.")

        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")

        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username exists.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif request.POST.get("terms") != "on":
            messages.error(request, "Please accept the terms.")

        else:
            try:
                validate_password(password)

                with transaction.atomic():

                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=username
                    )

                    company, created = Company.objects.get_or_create(
                        name=company_name
                    )

                    RecruiterProfile.objects.create(
                        user=user,
                        company=company,
                        designation=designation
                    )

                messages.success(request, "Recruiter account created successfully!")
                return redirect("rec_login")

            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)

    return render(request, "rec_signup.html")

@login_required
def post_job(request):
    if request.method == "POST":
    
        title = request.POST.get("title")
        location = request.POST.get("location")
        work_mode = request.POST.get("work_mode")
        job_type = request.POST.get("job_type")
        experience = request.POST.get("experience")
        salary_min = request.POST.get("salary_min") or None
        salary_max = request.POST.get("salary_max") or None
        description = request.POST.get("description")
        skills = request.POST.get("skills")
        duration = request.POST.get("duration", "")
        application_url = request.POST.get("application_url", "")
        job_role = request.POST.get("job_role")

        
        Job.objects.create(
            title=title,
            company=request.user.recruiterprofile.company.name,
            description=description,
            skills=skills,
            location=location,
            job_type=job_type,
            work_mode=work_mode,
            experience=experience,
            salary_min=salary_min,
            salary_max=salary_max,
            duration=duration,
            application_url=application_url,
            job_role=job_role,
        )

        messages.success(request, "Job posted successfully!")
        return redirect("post_job")
    return render(request, 'post_job.html')

@login_required
def rem_saved_jobs(request, saved_job_id):
    job = JobSwipe.objects.get(id=saved_job_id)
    job.delete()
    

    return redirect('saved_jobs_view')