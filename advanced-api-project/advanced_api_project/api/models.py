from django.db import models

# This file defines the data models for the API project.
class Author(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
