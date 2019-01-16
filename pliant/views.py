""" 
Views for Pliant.
"""
from django.shortcuts import render
from pliant import boxaccess as box


def blog(request):
    """ 
    Gets the blog.
    """
    content = box.get_blog_items()
    return render(request, 'blog.html', {'entries':content})

def blog_entry(request, entry_id):
    """ 
    A single entry for the blog.
    """
    entry = box.get_blog_entry(entry_id)
    return render(request, 'entry.html', {'entry':entry})

def case_studies(request):
    """ 
    Gets entries that are case studies.
    """
    entries = box.get_case_studies()
    return render(request, 'case_studies.html', {'entries': entries})

def file_share(request):
    """ 
    Box file share widget.
    """
    return render(request, 'file_share.html', {})
