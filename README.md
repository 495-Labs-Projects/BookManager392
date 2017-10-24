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

4.  Create and switch to a new branch in git called models. Add the following two relationships to the Book model:
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

5.  Go to the Author model and add the following validations, scopes and methods:

    ```python
    class QuerySet(models.QuerySet):
    	def alphabetical(self):
    		return self.order_by('last_name', 'first_name')

    objects = QuerySet.as_manager()

    def __str__(self):
    	return self.last_name + ', ' + self.first_name 
    ```

6. Now let's add the following validations to the Book model.

    ##### Proposal Date
    *   Add a validation so that the `proposal_date` is either the current date or some time in the past. (The reason is you shouldn't be allowed to record a proposal you haven't yet received.) You can add a validator to a field by adding 

    		validators=[<list of custom validator functions here>]

    ##### Contract Date
    *   Add a validation to `contract_date` to ensure it is either the current date or some time in the past. (The reason is you shouldn't be allowed to record a contract you haven't yet signed.)

    *   Also make sure that the `contract_date` is some time after the `proposal_date` as you can't sign contracts for books yet to be proposed. - ASK PROF.H

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

		    url(r'^authors$', views.AuthorList.as_view(), name='author_list'),
		    url(r'^authors/(?P<pk>\d+)$', views.AuthorDetail.as_view(), name='author_detail'),
		    url(r'^authors/new$', views.AuthorCreate.as_view(), name='author_new'),
		    url(r'^authors/edit/(?P<pk>\d+)$', views.AuthorUpdate.as_view(), name='author_edit'),
		    url(r'^authors/delete/(?P<pk>\d+)$', views.AuthorDelete.as_view(), name='author_delete'),

		    url(r'^publishers$', views.PublisherList.as_view(), name='publisher_list'),
		    url(r'^publishers/(?P<pk>\d+)$', views.PublisherDetail.as_view(), name='publisher_detail'),
		    url(r'^publishers/new$', views.PublisherCreate.as_view(), name='publisher_new'),
		    url(r'^publishers/edit/(?P<pk>\d+)$', views.PublisherUpdate.as_view(), name='publisher_edit'),
		    url(r'^publishers/delete/(?P<pk>\d+)$', views.PublisherDelete.as_view(), name='publisher_delete'),
		]

		```
This will essentially create all the URL's for the app that will be in the address bar. It will allow us to navigate between the pages. Note that the url's reference different views. These are the Django "controllers". We will make those next.

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

Becca - This is as far as I went with the Django stuff. I think here we should either give them the code to copy and paste into one of the folders and tell them to do the rest, or give them a link to a git repo where they can download the views and just look at them. After they create the views they should go on the web interface and continue with similar instructions to what you have here I think.

6. Within templates/books create a new file called book_detail.html. This new view will be the show page for an individual book. Copy and paste the code below into the new file. If you review the code below, you'll see that we use three different types of syntax:
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

7. Not sure if we should do list templates or not.
Also, not fully sure of the best way to teach forms. Should we build a simple form first and then show them how to link that to other files? Or should we start by showing them the best way?

8. Next, we need to add in forms so that we can create books, authors, and publishers in our system. In the books folder create a generic file called forms.py. Since our forms will map very closely to our models we will use forms.ModelForm. 

```python
from django import forms
from books.models import *

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["title", "year_published", "publisher", "authors"] 
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
```

1.  Now go to the web interface and add a new publisher: "Pragmatic Bookshelf". After that, go to the books section and add a new book: "Agile Web Development with Rails" which was published by Pragmatic Bookshelf in 2013\. Make sure to update the three date fields with dates that follow the validations for `proposal_date`, `contract_date`, and `published_date` from Part 1! **Note that you need to refer to the publisher by its id (1), rather than its name in the current interface**. Thinking about this, and some other problems with the current interface, we will begin to make the interface more usable, working now in a new branch called 'interface'

2.  We'll begin by adding some more publishers directly into the database using the command line. If we think back to the SimpleQuotes lab last week, the easiest way to insert new data is by opening a new command line tab in the same directory and running `rails db`. Then paste the publishers_sql and authors_sql code given so that we have multiple publishers and authors to choose from (and sharpen our db skills slightly). **Note**: do not add the first publisher since we have already added Pragmatic Bookshelf via the web interface; if you do you will get an error because they are already in the db with a id=1.

    ```sql
    -- SQL for authors
    INSERT INTO "authors" VALUES (1, 'Sam', 'Ruby', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (2, 'Dave', 'Thomas', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (3, 'Hal', 'Fulton', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (4, 'Robert', 'Hoekman', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (5, 'David', 'Hannson', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (6, 'Dante', 'Alighieri', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (7, 'William', 'Shakespeare', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "authors" VALUES (8, 'Jane', 'Austen', '2015-02-09 12:00:00', '2014-02-10 12:00:00');

    -- SQL for publishers
    INSERT INTO "publishers" VALUES (1, 'Pragmatic Bookshelf', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "publishers" VALUES (2, 'Washington Square Press', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "publishers" VALUES (3, 'Addison Wesley', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "publishers" VALUES (4, 'Everyman Library', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    INSERT INTO "publishers" VALUES (5, 'New Riders', '2015-02-09 12:00:00', '2014-02-10 12:00:00');
    ```

3.  The first thing we will do is switch the 'publisher_id' field (a text box where you are supposed to remember and type out the appropriate publisher's id) to a drop-down list. Now that we have some publishers in the system, go to the `_form` partial in the Books view and change the publisher_id text_field to the following line:

    ```erb
    <%= form.collection_select :publisher_id, Publisher.alphabetical, :id, :name %>
    ```

    Look at the new form on the web page. It's an improvement (I also like to convert the number_field for year_published to a straight text field, but not required), but it'd be a little nicer if it didn't default to the first publisher. Go to [apidock.com/rails](http://apidock.com/rails) and look up `collection_select` and see if there is an option that will prompt the user for input rather than just display the first record. Implement similar functionality for contract_date and published_date (which are not required). After fixing this, I'd recommend you save this work to your git repository.

4.  Of course, we also need to be able to select one or more authors for each book. In the `_form.html.erb` template for books, add in a partial that will create the checkboxes for assigning an author to a book. Add the line

    ```erb
    <%= render partial: 'authors_checkboxes' %>
    ```

    just prior to the submit button in the template.

    Within the `app/views/books` directory, create a new file called `_authors_checkboxes.html.erb` and add to it the following code:

    ```erb
    <%= for author in Author.alphabetical %>
      <%= check_box_tag "book[author_ids][]", author.id, @book.authors.include?(author) %>
      <%= author.name %>
    <%= end %>
    ```

    Note: in Rails 3 and above, `render` assumes by default you are rendering a partial, so you could just say `render 'authors_checkboxes'` here, but I want you to put the `:partial =>` in for now to reinforce the idea of partials.

    If you were to try and submit the data for this form, it would reject the information for the authors (You could check this by looking in the BookAuthor table). We will talk about this later in the course. For now, add `:author_ids` to the list of attributes that your controller will allow to be passed to your Book model. We can find that list in a private method called `book_params` at the bottom of the `BooksController` -- add `:author_ids` there. Because this is an array of ids, we need to let Rails know that with the code below:

    ```ruby
    # controllers/books_controller.rb
    def book_params
      params.require(:book).permit(:title, :year_published, :publisher_id, :author_ids => [])
    end
    ```

5.  In the show template for books, change the `@book.publisher_id` to `@book.publisher.name` so that we are displaying more useful information regarding the publisher. After that, add in a partial that will create a bulleted list of authors for a particular book. To do that, add the line:

    ```erb
    <%= render partial: 'list_of_authors' %>
    ```

    after the publisher information in the template and in the code. Then add a file called `_list_of_authors.html.erb` to the app/views/books directory. Within this new file add the following code:

    ```erb
    <%= pluralize(@book.authors.size, 'Author') %>
    ```

6.  After that, add some books to the system using the web interface. Given the authors added, there are some suggested books listed at the end of this lab, but you can do as you wish. View and edit the books to be sure that everything is worked as intended. Of course, looking at the books index page, we realize it too has issues; fix it so that the publisher's name is listed rather than the id (see previous step if you forgot how) and the books are in alphabetical order by using the alphabetical scope in the appropriate place in the books_controller. (Try it yourself, but see a TA if you are struggling on this last one for more than 5 minutes.)

    **BTW, have you been using git after each step? If not, time to do so...**

7.  Look at the partial `list_of_authors`. There are three things to take note of:

    1.  how the pluralize function adds an 's' at the end of author when there is more than one
    2.  how Ruby loops through the list of authors (note that the erb tags for the 'for' and 'end' tag do not have an equal sign)
    3.  how Rails' link_to tag is used to wrap the author's name in an anchor tag leading back to the author's details page.
8.  Before having the TA sign off, you decide to test the following: go to a book in the system, uncheck all the authors, and save. It saves 'successfully', but the list of authors remains unchanged. **Ouch**. Good thing we are testing this app pretty carefully. How do we fix this? First, we need to realize that this happens because if no values are checked for author_ids, then rails by default just doesn't submit the parameter `book[:author_ids][]`. We can force it to submit an empty array by default by adding to the book form (right after the form_for tag) the following line:

    ```erb
    <%= hidden_field_tag "book[author_ids][]", nil%>
    ```

    Once this is working (test it again to be sure), then you can merge the `interface` branch in git back into the `master` branch.

9.  (Optional, but recommended if you have time left in lab) Having developed the interface for books, go back to the`interface` branch and write your own partial for show template of the authors view so that it added a list of all the books the author has written. (This is very similar to what was done for the show book functionality and those instructions/code can guide you.) Once you know it is working properly, save the code to the repo and merge back into the master branch.

# <span class="mega-icon mega-icon-issue-opened"></span>Stop

Show a TA that you have completed the lab. Make sure the TA initials your sheet.

## On Your Own

This week the "on your own" assignment is to go to [RubyMonk's free Ruby Primer](http://rubymonk.com/learning/books/1) and complete any of the previously assigned exercises you have not yet done. If you are caught up and understand the previous exercises (repeat any you are unsure of), you may if time allows choose any of the other primer exercises and try to get ahead (we will do more of these exercises after the exam). Note: be aware that questions from RubyMonk can and will show up on the exam, so 'doing it on your own' does not mean 'doing it if you want to'.

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
