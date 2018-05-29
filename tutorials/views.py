from django.shortcuts import render


def index(request):
    return render(request, 'tutorials/introduction.html', {})


def introduction(request):
    return render(request, 'tutorials/introduction.html', {})


def select(request):
    return render(request, 'tutorials/select.html', {})


def insert(request):
    return render(request, 'tutorials/insert.html', {})


def update(request):
    return render(request, 'tutorials/update.html', {})


def create(request):
    return render(request, 'tutorials/create.html', {})


def constraints(request):
    return render(request, 'tutorials/constraints.html', {})
