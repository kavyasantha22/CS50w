from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(label = "Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    content = util.get_entry(name)
    if content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "name" : name,
            "entry" : content
        })

def search(request):
    query = request.GET.get("q").lower()

    content = util.get_entry(query)

    if (content == None):
        pages = util.list_entries()
        match = []
        for page in pages:
            if query in page.lower():
                match.append(page)
        return render(request, "encyclopedia/search.html", {
            "matched_result" : match
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name" : query,
            "entry" : content
        })
    
def create_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            avail_pages = util.list_entries()
            if title in avail_pages:
                return render(request, "encyclopedia/create_page.html", {
                "form" : NewPageForm(),
                "error_message" : "Title is already taken"
            })
            content = form.cleaned_data["content"]
            with open(f"entries/{title}.md", "w") as f:
                f.write(content)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/create_page.html", {
            "form" : NewPageForm()
        })

def edit_page(request, name):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            with open(f"entries/{title}.md", "w") as f:
                f.write(content)
            return render(request, "encyclopedia/edit_page.html", {
                    "form" : form,
                    "name" : name,
                    "message" : "Successfully updated the page"
                })
        else:
            return render(request, "encyclopedia/error.html")
    else:
        content = util.get_entry(name)
        if content is None:
            return render(request, "encyclopedia/error.html")
        else:
            form = NewPageForm(initial={"title":name, "content":content})
            return render(request, "encyclopedia/edit_page.html", {
                "form" : form,
                "name" : name
            })

def random_page(request):
    entries = util.list_entries()
    name = random.choice(entries)
    content = util.get_entry(name)
    if content is None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "name" : name,
            "entry" : content
        })


