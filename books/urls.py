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