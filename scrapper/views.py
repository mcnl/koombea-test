from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import SignUpForm, CustomAuthenticationForm
from .models import Page, Link
from .scrapper import Scraper


class SignUpView(View):
    form_class = SignUpForm
    template_name = "signup.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("add_page")

        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "login.html"


class AddPageView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"
    template_name = "add_page.html"
    scraper = Scraper()

    def get(self, request):
        pages = Page.objects.filter(user=request.user)
        paginator = Paginator(pages, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj})

    def post(self, request):
        link = request.POST.get("link")

        if link:
            self.scraper.add_page(request.user, link)

        return redirect("add_page")


class PageDetailView(LoginRequiredMixin, DetailView):
    login_url = "login"
    model = Page
    template_name = "page_detail.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = self.object.links.all()
        context["links"] = links

        return context
