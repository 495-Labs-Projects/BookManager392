## Part 1

1. Create a new Django project called "BookManager":

	```git
	django-admin startproject BookManager
	```

2. Switch directories (`cd`) into this Django app from the command line. You should see the manage.py file. In that directory, type the following to create the app:

	```git
	python manage.py startapp books
	```

3. Create a git repository, add and commit the initial files with the commit message "Initial commit".

4. Go into the settings.py file and add the following line into INSTALLED_APPS:

	```python
	'books.apps.BooksConfig'
	```

to register your app in the project.

5. Add a new requirements.txt file with your favorite text editor at the highest level of your project, and add the following:
	```python
	appdirs==1.4.3
	coverage==4.4.1
	Django==1.11.1
	factory-boy==2.8.1
	Faker==0.7.12
	packaging==16.8
	pdb==0.1
	pyparsing==2.2.0
	python-dateutil==2.6.0
	python-gnupg==0.4.0
	pytz==2017.2
	PyYAML==3.12
	selenium==3.4.2
	six==1.10.0
	```

6. Install the requirements by running

	```git
	pip install -r requirements.txt
	```

7. We will create three models and their database fields. This is the code for the Book model, which goes in models.py. Note that blank=true means that the field is NOT required, while not including this field means the field is required. 
	
	```python
	from datetime import date
	class Book(models.Model):
		# Book fields
		title = models.CharField(max_length=255)
		proposal_date = models.DateField(default=datetime.now, blank=True)
		contract_date = models.DateField(default=datetime.now, blank=True)
		published_date = models.DateField(default=datetime.now, blank=True)
		units_sold = models.IntegerField(default=0, blank=True)
	```


8. Next, work on creating the models for Publisher and Author in the same file. The fields are as follows:

    ### Publisher

    *   name (string) - required

    ### Author

    *   first_name (string) - required
    *   last_name (string) - required



9. After creating these models, migrate the database by running the following and save all this generated code to git.

	 ```git
	 python manage.py makemigrations books
	 python manage.py migrate
	 ```

10.  Create and switch to a new branch in git called models. Add the following two relationships to the Book model:

   ```python
   publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
   authors = models.ManyToManyField(Author) 
   ```

Then, add the following scope:

  ```python
  class QuerySet(models.QuerySet):
    def alphabetical(self):
    	return self.order_by('title')

  objects = QuerySet.as_manager()
  ```

It's also good practice in Django to always add an str method to every model to make debugging easier. You would do so with the following: 

  ```python
  def __str__(self):
  	return self.title
  ```

Feel free to do so for every model you create.

11.  Go to the Author model and add the following validations, scopes and methods:

   ```python
   class QuerySet(models.QuerySet):
    def alphabetical(self):
  	  return self.order_by('last_name', 'first_name')

   objects = QuerySet.as_manager()

   def __str__(self):
  	 return self.last_name + ', ' + self.first_name 
   ```

12. Now let's add the following validations to the Book model.

    ##### Proposal Date
    *   Add a validation so that the `proposal_date` is either the current date or some time in the past. (The reason is you shouldn't be allowed to record a proposal you haven't yet received.) You can add a validator to a field by adding 

    		validators = [<list of custom validator functions here>]

    ##### Contract Date
    *   Add a validation to `contract_date` to ensure it is either the current date or some time in the past. (The reason is you shouldn't be allowed to record a contract you haven't yet signed.)

    *   Also make sure that the `contract_date` is some time after the `proposal_date` as you can't sign contracts for books yet to be proposed.

    You would use the clean() method to compare two different fields. You can do so with the following code:

    ```python
    def clean(self):
	    if self.contract_date <= self.proposal_date:
	      raise ValidationError(
	            _('Contract date (%(value2)) should be after proposal date (%(value))'),
	          params={'value': self.proposal_date, 'value2': self.contract_date},
	        )
    ```

    ##### Published Date
    *   Add a validation to `published_date` so that it is also either the current date or some time in the past.

    *   Also make sure that the `published_date` is some time after the `contract_date` as you can't publish books without contracts.

* * *

# <span class="mega-icon mega-icon-issue-opened"></span>Stop

Show a TA that you have the basic Django app set up and working, and that you have properly saved the code to git. Make sure the TA initials your sheet.

* * *

## Part 2

1. Next, go into BookManager -> urls.py, and replace with the following to make sure that all pages in the books app are under the book/ url path.

	 ```python
		 from django.conf.urls import url
		 from django.conf.urls import include
		 from django.contrib import admin

		 urlpatterns = [
		     url(r'^admin/', admin.site.urls),
		     url(r'^books/', include('books.urls', namespace='books')),
		 ]
	 ```

2. Go back into books app and create a new file called urls.py. Add the following to it:

	 ```python
		 from django.conf.urls import url

		 from books import views

		 urlpatterns = [
		     url(r'^$', views.BookList.as_view(), name='book_list'),
		     url(r'^(?P<pk>\d+)$', views.BookDetail.as_view(), name='book_detail'),
		     url(r'^new$', views.BookCreate.as_view(), name='book_new'),
		     url(r'^edit/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_edit'),
		     url(r'^delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name='book_delete'),
        
         ...
     ]

	 ```

This will essentially create all the URL's for the app that will be in the address bar. It will allow us to navigate between the pages. Note that the url's reference different views. These are the Django "controllers". We will make those next.

Now write similar url's for Authors and Publishers. Ask a TA if you are confused.

3. Go to the views.py file within the books app. Here we will create class views. What this means is we will create view-controllers for the different CRUD operations for each model. First, add the following imports at the top of your file:

   ```python
     from django.shortcuts import get_object_or_404, render
		 from django.http import HttpResponseRedirect
		 from django.urls import reverse
		 from django.contrib import messages

		 from django.views.generic import View, TemplateView, ListView
		 from django.views.generic.detail import DetailView
		 from django.views.generic.edit import CreateView, UpdateView, DeleteView

		 from books.models import *
		 from books.forms import *
   ```

4. The following are the class based CRUD operations for Publisher. You can copy this into your file. Then, do the same for Book and Author in views.py. 

List view will give a list of all publishers (think of index in rails), detail is similar to a 'show' page, and the rest are the CRUD operations for the model. You will notice that each defines different HTTP methods that it will respond to. Within those, necessary variables are created in a context that is then passed on to the rendered template.

	 ```python
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
		```

5. Now that we have URL's and views, we need to create the templates that will be rendered for those views. Keep in mind that Django has a lot less "magic" than Rails, so a lot of the low level work has to be done where Rails scaffolding may have created it all for you. At the same time, this allows for more customization in Django, which is the reason it is so popular.

First, create a folder named 'templates' inside books. Within templates, create folders for authors, books, and publishers.

Next, create a templates folder in the outer directory. You can get the files from the following link: < placeholder >

and add them to this folder.

6. Before any templates will be able to load, we need to add a few things to the top level BookManager so that it knows to look in books for the templates. First, go to urls.py in BookManager and add the following (or replace if already there):

```python
url(r'^books/', include('books.urls', namespace='books')),
```

Next, go to settings.py and replace the TEMPLATES variable with the following:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates').replace('\\','/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

7. Now we are ready to create some templates. Within templates/books create a new file called book_detail.html. This new view will be equivalent to the rails show page for an individual book. Copy and paste the code below into the new file. If you review the code below, you'll see that we use three different types of syntax:
 1) Basic HTML
 2) {%%} - use to run python code
 3) {{}} - use to evaluate and display variable attributes
After completing this process for books, follow the same procedure for authors and publishers.

```html
{% extends "books_base.html" %}

{% block content %}

<h1 id="book-title">{{ object.title }}</h1>

<p>Year Publsihed: {{ object.year_published }}</p>
<p>Publisher: {{ object.publisher.name }}</p>

<p>
    Authors:
    <ul id="book-authors">
    {% for author in object.authors.all %}
        <li><a href="{% url 'books:author_detail' author.id %}">{{ author }}</a></li>
    {% endfor %}
    </ul>
</p>

<a href="{% url 'books:book_list' %}">Back to List</a>

{% endblock %}
```

8. We should also add in the equivalent of index pages for our different models to that we can see lists of books, authors, and publishers. Create a new file called book_list.html inside books/templates/books and include the following:

```html
{% extends "books_base.html" %}

{% block content %}

<h1>Books</h1>

{% if object_list %}
    <ul id="book-list">
        {% for book in object_list %}
        <li>
            <a href="{% url 'books:book_detail' book.id %}">{{ book.title }}</a>
            <a href="{% url 'books:book_edit' book.id %}">edit</a>
            <a href="{% url 'books:book_delete' book.id %}">delete</a>
        </li>
        {% endfor %}
    </ul>
{% else %}
    <p>No books are available.</p>
{% endif %}

<a href="{% url 'books:book_new' %}">New</a>

{% endblock %}
```
Make sure to create list pages for author and publisher as well.

9. Since we have now given the user the ability to delete objects, let us also make sure that we have a confirmation for them before they actually delete an object. For authors create a new file in books/templates/author called author_confirm_delete.html and include: 

```html
{% extends "books_base.html" %}

{% block content %}

<form method="post">{% csrf_token %}
    Are you sure you want to delete "{{ object }}" ?
    <input type="submit" value="Submit" />
</form>

{% endblock %}
```

Accordingly, we'll need to update our views.py file so that we see the new confirmation when we try to delete an author: 

```python
class AuthorDelete(DeleteView):
    model = Author
    template_name = 'authors/author_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('books:author_list')
```

Once again, make sure you complete these steps for book and publisher yourself.

10. Next, we need to add in forms so that we can create and books, authors, and publishers in our system. In the books folder create a generic file called forms.py. Since our forms will map very closely to our models we will use forms.ModelForm. The following is the code for author. Create the same class structure for books and publishers.

```python
from django import forms
from books.models import *

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["first_name", "last_name"]  
```

11. Once again we need to create views for our forms. Going back to books/templates/publishers create a new file called publisher_form.html:

```html

{% extends "books_base.html" %}

{% block content %}

<form method="post">{% csrf_token %}
    {{ form.non_field_errors }}
    <p>
        {{ form.name.errors }}
        <label for="{{ form.name.id_for_label }}">Name:</label>
        {{ form.name }}
    </p>

    {% if publisher %}
        <input type="submit" value="Update Publisher" />
    {% else %}
        <input type="submit" value="Create Publisher" />
    {% endif %}
</form>

{% endblock %}


```

12. In the publisher form we created a field for each attribute in our model. In this case, we only had to create a form field for name. But if we had a model with lots of fields our form could get very messy. Instead we can use a django shortcut, form.as_p to render all of the fields in html p tags. Let's create the author form this way:

```html
{% extends "books_base.html" %}

{% block content %}

<form method="post">{% csrf_token %}
    {{ form.as_p }}
    {% if object %}
        <input type="submit" value="Update Author" />
    {% else %}
        <input type="submit" value="Create Author" />
    {% endif %}
</form>

{% endblock %}
```
Follow the same procedure for book as well.

13. Lastly, the book form contains a list of authors and the user should be able to select one to many authors for the book. To ensure the form works this way, let's update the book model in the forms.py file to be:

```python
class Meta:
        model = Book
        fields = ["title", "year_published", "publisher", "authors"] 
        widgets = {
            'authors': forms.CheckboxSelectMultiple,
        }
```

This way the form will render the authors as a list of checkboxes from which the user can select multiple.

14. Now let's check out the admin panel. The admin panel is an interface that Django provides for you to interact with the database directly. You can access it from localhost by adding '/admin' to your url. The first step to be able to get into the admin portal is to create a superuser that has access to it. To do this, you would type in

```git
python manage.py createsuperuser
```

in the top level directory. Then you can follow the steps to create a username, email, and password. Make sure to run the server. Then you can go to '/admin' and you should see "Django administration" with a login form.

15. Notice that you currently can't see any of your models. This is because we need to allow the admin to access each model. To do this, go to the admin.py file in books and add the following:

```python
from books.models import *
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
```

Re-run the server and you should now see all the models in the admin portal.

16. Create two authors, a publisher, and a book using the admin portal. Note that you can pick more than one author for each book.

17. Finally, ensure that you commit all your changes to git and merge branches to master. You should be able to see the models on the interface after adding them in the admin portal. Feel free to play around and add some more of the books below to get familiar with the admin portal, or work on making the interface better if you have extra time.

# <span class="mega-icon mega-icon-issue-opened"></span>Stop

Show a TA that you have completed the lab. Make sure the TA initials your sheet.

* * *

## Suggested Books

**Agile Web Development with Rails**

*   Year published: 2011
*   Publisher: Pragmatic Bookshelf
*   Authors:
    *   Sam Ruby
    *   David Hannson
    *   Dave Thomas

**Romeo and Juliet**

*   Year published: 2004
*   Publisher: Washington Square Press
*   Authors:
    *   William Shakespeare

**King Lear**

*   Year published: 2004
*   Publisher: Washington Square Press
*   Authors:
    *   William Shakespeare

**The Divine Comedy**

*   Year published: 1995
*   Publisher: Everyman's Library
*   Authors:
    *   Dante Alighieri

**Pride and Prejudice**

*   Year published: 2001
*   Publisher: Washington Square Press
*   Authors:
    *   Jane Austen
