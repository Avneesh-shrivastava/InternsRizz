from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.http import JsonResponse

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
            username=username,
            password=password
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
    data = json.loads(request.body)
    jobs = Job.objects.all()
    # job_id = data.get("job_id")
    decision = data.get("decision")

    try:
        # Read the data sent by JavaScript fetch()
        data = json.loads(request.body)

        job_id = data.get("job_id")
        decision = data.get("decision")

        # Validate the decision
        if decision not in [
            "interested",
            "not_interested",
            "saved"
        ]:
            return JsonResponse(
                {"error": "Invalid decision."},
                status=400
            )

        # Find the job
        job = Job.objects.get(id=job_id, is_active=True)

        # Save or update the user's decision
        swipe, created = JobSwipe.objects.update_or_create(
            user=request.user,
            job=job,
            defaults={"decision": decision}
        )

        return JsonResponse({
            "success": True,
            "decision": swipe.decision
        })

    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400
        )

    except Job.DoesNotExist:
        return JsonResponse(
            {"error": "Job not found."},
            status=404
        )


    return render(
        request,
        "job_feed.html",
        {
            "jobs": jobs
        }
    )