import re, markdown2

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django import forms

from . import util


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
            "content": markdown2.markdown(f)
        })

def search(request, q):
    e = util.list_entries()
    c = re.compile(e, re.IGNORECASE)
    results = re.finditer(q)
    if results is not None:
        return render(request, "encyclopedia/search.html", {
            "results": results
        })
