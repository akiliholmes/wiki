import re, markdown2, secrets

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    f = util.get_entry(title)
    if f == None:
        raise Http404("Entry does not exist")
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdown2.markdown(f)
        })

def search(request):
            data = request.GET.get('q','')
            if util.get_entry(data) is not None:
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[data]))
            else:
                partialEntries = []
                for entry in util.list_entries():
                    if data.upper() in entry.upper():
                        partialEntries.append(entry)
                return render(request, "encyclopedia/search.html",{
                    "results": partialEntries
                })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            f = util.get_entry(title)
            if f == None:
                create = util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
            else:
                return render(request, "encyclopedia/new.html", {
                    "error": "This entry already exist",
                    "form": form
                    })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })

def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            create = util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        f = util.get_entry(title)
        data = {'title': f'{title}', 'content': f'{f}'}
        form = NewEntryForm(initial=data)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "form": form
        })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return render(request, "encyclopedia/entry.html",{
        "title": randomEntry,
        "content": markdown2.markdown(util.get_entry(randomEntry))
    })
