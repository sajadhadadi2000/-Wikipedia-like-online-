from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random
import re
from . import util
from .forms import Search, NewPage

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, title):
    # Getting query 
    q = util.get_entry(title=title)
    # If there was an entry
    if q == None:
        return render(request, "encyclopedia/404.html", { "context" : title })
    else:
        # If there is no entry
        markdowner = Markdown()
        context = markdowner.convert(q)
        return render(request, "encyclopedia/page.html", { "context" : context, "title" : title })


def searchviwe(request):
    # Getting query  
    
    if request.method == 'GET':
        form = Search(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
    # Checking the existence of the entry and redirecting directly to it
    q = util.get_entry(query)
    if q != None:
        markdowner = Markdown()
        context = markdowner.convert(q)
        return render(request, "encyclopedia/page.html", { "context" : context, "title" : query })
    else:
        # Search query in existing entries
        all_entries =  util.list_entries()
        
        entries = ""
        for entry in all_entries:
            entries += " " + str(entry)

        r = r"\w*" + query + r"\w*" 
        context = re.findall(r, entries)
        title = "Search results for '{}'"
        if len(context) != 0 :
            return render(request, "encyclopedia/result.html", { "context" : context, "title" : title.format(query) })
        else:
            return render(request, "encyclopedia/noresult.html", { "title" : title.format(query) })

def createpage(request):
    # Getting title and content
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            # Checking the availability of the entry (save or error message)
            if util.get_entry(title) == None:
                # Save entry
                util.save_entry(title, content)
                return HttpResponseRedirect('/wiki/{}'.format(title))
            else:
                # Error massage 
                return render(request, "encyclopedia/entryerror.html", { "title" : title })
    else:
        return render(request, "encyclopedia/createpage.html")


def randpage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect('/wiki/{}'.format(title))

def editpage(request, title):
    # Getting title and content
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect('/wiki/{}'.format(title))
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {'context' : content , 'title': title })
