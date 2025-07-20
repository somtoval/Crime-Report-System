# Import necessary modules
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import (
    authenticate,
    login as authLogin,
    logout as authLogout,
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import CrimeReport, CrimeCategory, Suspect, Evidence, Case, Victim
from functools import wraps


def guest_only(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return _wrapper


def login_required(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapper


@guest_only
def login_view(
    request,
):
    """
    Handles user login attempts.

    - Displays the login form on GET request.
    - Processes login credentials on POST request.
    - Authenticates the user and logs them in if valid.
    - Displays errors if login fails or form is invalid.
    """
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Process the data in form.cleaned_data
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")  # Use cleaned data

            # Authenticate the user
            user = authenticate(
                request, username=username, password=password
            )  # Pass request to authenticate

            if user is not None:
                # Log the user in
                authLogin(request, user)
                messages.success(
                    request, f"Welcome back, {username}!"
                )  # Optional success message
                # Redirect to a success page (e.g., dashboard)
                return redirect(
                    "dashboard"
                )  # Replace "dashboard" with your target URL name
            else:
                # Invalid login credentials
                messages.error(
                    request, "Invalid username or password. Please try again."
                )
                # No redirect here, just fall through to render the form again with errors
        else:
            # Form validation failed
            messages.error(request, "Please correct the errors below.")
            # No redirect here, the invalid form will be passed to the template

    else:  # GET request
        # Create a blank form instance
        form = LoginForm()

    # Render the login page with the form (either blank or with errors)
    return render(request, "login.html", {"form": form})


@guest_only
def signup(request):
    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            password2 = form.cleaned_data.get("password2")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken")
                return redirect("signup")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email address is taken")
                return redirect("signup")

            if password != password2:
                messages.error(request, "Both passwords do not match")
                return redirect("signup")

            user = User.objects.create(
                email=email, username=username, password=make_password(password)
            )

            authLogin(request, user)
            return redirect("dashboard")
        else:
            # Form validation failed
            messages.error(request, "Please correct the errors below.")
            # No redirect here, the invalid form will be passed to the template
    else:
        form = SignupForm()

    return render(request, "signup.html")


@login_required
def logout(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        authLogout(request)
        return redirect("login")
    return render(request, "logout.html")


# ##########################################
# User Views
# ##########################################
@login_required
def dashboard(request):
    user_reports = CrimeReport.objects.filter(reporter=request.user).order_by(
        "-reported_at"
    )
    context = {
        "user_reports": user_reports,
    }
    return render(request, "user/index.html", context)


@login_required
def file_report(request):
    crime_categories = CrimeCategory.objects.all()
    if request.method == "POST":
        location = request.POST["location"]
        crime_category_id = request.POST.get("crime_type")
        crime_time = request.POST["crime_time"]
        description = request.POST["description"]

        crime_category = None
        if crime_category_id:
            try:
                crime_category = CrimeCategory.objects.get(id=crime_category_id)
            except CrimeCategory.DoesNotExist:
                messages.error(request, "Invalid crime type selected.")
                return render(
                    request,
                    "user/file_report.html",
                    {"crime_categories": crime_categories},
                )

        CrimeReport.objects.create(
            reporter=request.user,
            location=location,
            crime_type=crime_category,
            crime_time=crime_time,
            description=description,
        )
        messages.success(request, "Your report has been filed successfully.")
        return redirect("my_reports")  # Redirect to My Reports or Dashboard

    return render(
        request, "user/file_report.html", {"crime_categories": crime_categories}
    )


@login_required
def my_reports(request):
    user_reports = CrimeReport.objects.filter(reporter=request.user).order_by(
        "-reported_at"
    )
    context = {
        "user_reports": user_reports,
    }
    return render(request, "user/my_reports.html", context)


@login_required
def report(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id, reporter=request.user)
    context = {
        "report": report,
    }
    return render(
        request, "user/report_detail.html", context
    )  # Changed template name for clarity


@login_required
def notifications(request):
    # In a real application, you would fetch notifications relevant to the user
    context = {
        "notifications": [],  # Replace with actual notifications
    }
    return render(request, "user/notifications.html", context)


@login_required
def profile_settings(request):
    # You would typically fetch user profile information here
    return render(request, "user/profile_settings.html")


def help_support(request):
    return render(request, "user/help_support.html")
