from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Report
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from allauth.socialaccount.views import RedirectAuthenticatedUserMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from .forms import InputForm
from .models import Report
from django.contrib.auth.decorators import login_required


def google_login(request):
    return redirect(reverse_lazy('login:welcome'))

def login(request):
    return render(request, "login/login_page.html")
    # return HttpResponse("this will be the login page")

def welcome_page(request):
    return render(request, "login/welcome_page.html")


@login_required
def view_reports(request):
    # Fetch the currently logged-in user
    curr_user = request.user

    # Retrieve the reports submitted by the current user
    user_reports = Report.objects.filter(username=curr_user.username)

    # Pass the user_reports to the template for rendering
    context = {
        'user_reports': user_reports
    }

    return render(request, "login/view_reports.html", context)

# update to pass the user
def home(request):
    load_admin = False
    curr_username = "DEFAULT123"
    curr_user = None

    try:
        login_email = request.user.email
        is_defined_user = User.objects.filter(email=login_email).exists()

        if not is_defined_user:
            user = User(email=login_email, username=request.user.username)
            user.save()
        else:
            curr_username = User.objects.get(email=login_email).username
            curr_user = User.objects.get(email=login_email)
            if User.objects.get(email=login_email).is_admin:
                load_admin = True
    finally:
        if load_admin:
            context = {
                "all_reports": Report.objects.all(),
                "resolved_reports": Report.objects.filter(resolved=True),
                "unresolved_reports": Report.objects.filter(resolved=False),
            }
            return render(request, "login/admin_home.html", context)
        else:
            user_reports = curr_user.get_reports() if curr_user else None  # Retrieve user's previous submissions
            if request.method == 'POST':
                form = InputForm(request.POST, request.FILES)
                if form.is_valid():
                    set_username = curr_username if curr_username != "DEFAULT123" else "(anonymous)"
                    report = Report(
                        username=set_username,
                        full_name=form.cleaned_data['full_name'],
                        incident_type=form.cleaned_data['incident_type'],
                        description=form.cleaned_data['description'],
                        location=form.cleaned_data['location'],
                        images=form.cleaned_data['images'],
                        videos=form.cleaned_data['videos']
                    )
                    report.save()
                    return HttpResponseRedirect(reverse("login:submission", args=(report.id,)))
                form = InputForm()
                return render(request, "login/home_page.html", {'form': form, 'user_reports': user_reports})
            else:
                form = InputForm()
                return render(request, "login/home_page.html", {'form': form, 'user_reports': user_reports})


def logout_view(request):
    logout(request)
    return redirect("/login")

def see_submission(request, report_id):
    # Get the report, or 404 if not found
    report = get_object_or_404(Report, pk=report_id)

    # Assume the user is not an admin until verified
    is_admin = False

    # Check if the user is logged in
    if request.user.is_authenticated:
        # Check if there's a User entry for the current logged-in user's email
        logged_in_user = User.objects.filter(email=request.user.email).first()
        if logged_in_user:
            is_admin = logged_in_user.is_admin

            # If the user is an admin and the report is 'new', update status to 'in_progress'
            if is_admin and report.status == 'new':
                report.status = 'in_progress'
                report.save()

    context = {
        "report": report,
        "is_admin": is_admin
    }
    return render(request, "login/view_submission.html", context)


def resolve_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    report.resolved = True
    report.save()
    return redirect(reverse_lazy('login:home'))


def update_notes(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_notes = request.POST.get('notes')

        # Retrieve the report object
        report = get_object_or_404(Report, id=report_id)

        # Update the notes field
        report.notes = new_notes

        # Save the changes to the database
        report.save()

    # Redirect back to the admin home page
    return redirect('login:home')