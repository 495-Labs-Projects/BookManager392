from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.views.generic import View, TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from books.models import *
from books.forms import *

# Books CRUD operations
# (Note: Check out at the bottom the CRUD operations for Publisher if you want to see the 
# detailed version of what is done with Book and Publisher)
#
# The CRUB operations for Books uses generic Class Based Views which generalizes a lot
# of the interactions. Classes like ListView just displays a list (given a queryset) and
# CreateView displays the new form and creates a new item (in this case a Book).
# ListViews and DetailView only responds to GET requests, because they only display things.
# CreateView and UpdateView responds to both GET and POST requests, GET for the form (new/edit),
# and POST for the actual creation (create/update).
# DeleteView also responds to both GET and POST, GET for the delete confirmation (check the template),
# and POST for the actual deletion. 

class BookList(ListView):
    model = Book()

    def get_queryset(self):
        return Book.objects.alphabetical()

class BookDetail(DetailView):
    model = Book

class BookCreate(CreateView):
    model = Book
    form_class = BookForm

    def get_success_url(self):
        return reverse('books:book_detail', args=(self.object.id,))

class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    
    def get_success_url(self):
        return reverse('books:book_detail', args=(self.object.id,))

class BookDelete(DeleteView):
    model = Book
    
    def get_success_url(self):
        return reverse('books:book_list')


# Author CRUD operations

class AuthorList(ListView):
    model = Author
    template_name = 'authors/author_list.html'

    def get_queryset(self):
        return Author.objects.alphabetical()

class AuthorDetail(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_form.html'

    def get_success_url(self):
        return reverse('books:author_detail', args=(self.object.id,))

class AuthorUpdate(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_form.html'
    
    def get_success_url(self):
        return reverse('books:author_detail', args=(self.object.id,))

class AuthorDelete(DeleteView):
    model = Author
    template_name = 'authors/author_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('books:author_list')


# Publisher CRUD operations
# All the CRUD actions for Publisher is broken down to use just the View Class. 
# This does basically the same exact thing as the CRUD views for Book and Author, but
# this has a lot more code explaining what is actually going on. This is probably better
# for educational use. 
# This is just the more detailed written out version of what could be simply done with 
# class based views.

class PublisherList(View):

    def get(self, request):
        template = 'publishers/publisher_list.html'
        context = {
            'publishers': Publisher.objects.alphabetical()
        }
        return render(request, template, context)

class PublisherDetail(View):

    def get(self, request, pk):
        template = 'publishers/publisher_detail.html'
        publisher = get_object_or_404(Publisher, pk=pk)
        context = {
            'publisher': publisher
        }
        return render(request, template, context)

class PublisherCreate(View):

    def get(self, request):
        template = 'publishers/publisher_form.html'
        form = PublisherForm()
        context = {
            'form': form
        }
        return render(request, template, context)

    def post(self, request):
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, 'Sucessfully created %s!' % publisher.name)
            return HttpResponseRedirect(reverse('books:publisher_detail', args=(publisher.id,)))
        else:
            template = 'publishers/publisher_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class PublisherUpdate(View):

    def get(self, request, pk):
        template = 'publishers/publisher_form.html'
        publisher = get_object_or_404(Publisher, pk=pk)
        form = PublisherForm(instance=publisher)
        context = {
            'publisher': publisher,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, 'Sucessfully updated %s!' % publisher.name)
            return HttpResponseRedirect(reverse('books:publisher_detail', args=(publisher.id,)))
        else:
            template = 'publishers/publisher_form.html'
            context = {
                'form': form
            }
            return render(request, template, context)

class PublisherDelete(View):

    def post(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        publisher.delete()
        messages.success(request, 'Sucessfully deleted %s!' % publisher.name)
        return HttpResponseRedirect(reverse('books:publisher_list'))