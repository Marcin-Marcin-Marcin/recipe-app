from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


def login_view(request):
    error_message = None

    next_url = request.GET.get("next") or "recipes:recipes_overview"

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.POST.get("next") or "recipes:recipes_overview"
            return redirect(next_url)

        error_message = "Invalid username or password."
    else:
        form = AuthenticationForm()

    context = {"form": form, "error_message": error_message, "next": next_url}
    return render(request, "auth/login.html", context)


def logout_view(request):
    """
    Logs the user out and redirects to a 'successfully logged out' page.
    """
    logout(request)
    return redirect("success")


def success_view(request):
    """
    Page shown after logging out.
    """
    return render(request, "auth/success.html")
