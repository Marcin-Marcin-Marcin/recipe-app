from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


def login_view(request):
    error_message = None

    # Prefer ?next=/some/path/ but fall back to recipes list
    next_url = request.GET.get("next") or request.POST.get("next") or "/recipes/"

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            # Safety: only allow redirects to safe hosts/paths
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)

            return redirect("/recipes/")

        error_message = "Invalid username or password."
    else:
        form = AuthenticationForm()

    context = {"form": form, "error_message": error_message, "next": next_url}
    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("success")


def success_view(request):
    return render(request, "auth/success.html")


def about_view(request):
    return render(request, "about.html")
