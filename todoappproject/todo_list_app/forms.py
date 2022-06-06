from django import forms

from todoappproject.todo_list_app.models import Task

#  Custom form
# class TaskCreateForm(forms.ModelForm):
#
#     class Meta:
#         model = Task
#         fields = ('title', 'description')
#         labels = {
#             'title': 'Title',
#             'description': 'Description',
#         }
