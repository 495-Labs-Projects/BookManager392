from django import forms
from books.models import *

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["title", "published_date", "publisher", "authors"] 
        widgets = {
            'authors': forms.CheckboxSelectMultiple,
        }


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["first_name", "last_name"] 


class PublisherForm(forms.ModelForm):
    
    class Meta:
        model = Publisher
        fields = ["name"] 
