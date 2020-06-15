from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth import login, authenticate, logout
from django.core.checks import messages
from django.shortcuts import render, HttpResponseRedirect, reverse

from file.forms import LoginForm, RegistrationForm, AddFileForm
from file.models import FileSystem


def index(request):
    return render(request, 'index.html', {'files': FileSystem.objects.all()})


def fileformview(request):
    html = 'addfile.html'
    form = AddFileForm()
    if request.method == "POST":
        form = AddFileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            FileSystem.objects.create(
                name=data['name'],
                parent=data['parent']
            )
            return HttpResponseRedirect(reverse('home'))

    return render(request, html, {"form": form})


def registration_view(request):
    html = 'register.html'
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(
                username=username,
                password=raw_password
            )
            login(request, account)
            return HttpResponseRedirect(
                request.GET.get(next, reverse('home'))
            )
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, html, context)


def loginview(request):
    html = 'login.html'
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password'],
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get(reverse('home'))
                )
        else:
            context['login_form'] = form
    else:
        form = LoginForm()
        context['login_form'] = form
    return render(request, html, context)


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def folder_view(request):
    folders = File.objects.all()
    return render(request, "index.html", {"folders": folders})
