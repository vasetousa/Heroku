from django.contrib import admin

# Register your models here.
from todoappproject.todo_list_app.models import Task

admin.site.register(Task)