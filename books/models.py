# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError # For custom validator errors
from django.utils.translation import ugettext_lazy as _ # For error message printing

class Publisher(models.Model):
  # Publisher fields
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Author(models.Model):
  # Author fields
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  # Author scopes
  class QuerySet(models.QuerySet):
    def alphabetical(self):
      return self.order_by('last_name', 'first_name')

  objects = QuerySet.as_manager()

  def __str__(self):
    return self.last_name + ', ' + self.first_name 



# Create your models here.
class Book(models.Model):
  # Book validators
  def validate_past_date(date):
    if date >= timezone.now():
        raise ValidationError(
            _('%(value)s is in the future'),
            params={'value': date},
        )

  def clean(self):
    if self.contract_date <= self.proposal_date:
      raise ValidationError(
            _('Contract date (%(value2)) should be after proposal date (%(value))'),
          params={'value': self.proposal_date, 'value2': self.contract_date},
        )
    if self.published_date <= self.contract_date:
      raise ValidationError(
          _('Proposal date (%(value2)) should be after contract date (%(value))'),
          params={'value': self.contract_date, 'value2': self.published_date},
      )

  # Book fields
  title = models.CharField(max_length=255)
  proposal_date = models.DateField(default=timezone.now(), blank=True, validators=[validate_past_date])
  contract_date = models.DateField(default=timezone.now(), blank=True, validators=[validate_past_date])
  published_date = models.DateField(default=timezone.now(), blank=True, validators=[validate_past_date])
  units_sold = models.IntegerField(default=0, blank=True)

  # Book relationships
  publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
  authors = models.ManyToManyField(Author)

  # Book scopes
  class QuerySet(models.QuerySet):
    def alphabetical(self):
      return self.order_by('title')

  objects = QuerySet.as_manager()

  def __str__(self):
    return self.title

