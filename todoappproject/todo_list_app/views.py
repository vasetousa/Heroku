from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

# Create your views here.
# from todoappproject.todo_list_app.forms import TaskCreateForm
from todoappproject.todo_list_app.models import Task

'''
- Adding the LoginRequiredMixin helps restrict direct access to pages from the address field
- overwriting the get_context_data() method provides a way to restrict the logged user from 
seeing other user's items.
'''


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'  # changes the name 'object_name' in the HTML to whatever name you choose

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)  # overwriting for logged user ONLY!
        context['count'] = context['tasks'].filter(complete=False).count()  # completed tasks count (False by default)

        search_input = self.request.GET.get('search-area') or ''    # this is the search area field
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input   # use title__icontains to filter by starting letter
            )
        context['search_input'] = search_input     # search area when refreshing the page
        return context                             # is done automatically


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo_list_app/task.html'


'''
- Overwriting the form_valid method will help us create tasks for the logged User ONLY!
Also, remove the field '__all__' (if used)  and replace it with the list of fields you want to see in the django
form.
'''


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']  # replace with a list of fields
    success_url = reverse_lazy('tasks')

    # form_class = TaskForm  # use with custom form for the creation

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


# Use when custom form is used
# class TaskCreate(CreateView):
#     model = Task
#     # fields = '__all__'
#     success_url = reverse_lazy('tasks')
#     template_name = 'todo_list_app/task_form.html'
#     form_class = TaskCreateForm  # use if an own form is used for the creation


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class CustomLoginView(LoginView):
    template_name = 'todo_list_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'todo_list_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()  # loging the user directly,
        if user is not None:  # not requiring additional login
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):  # redirects the user to 'tasks' if manual change
        if self.request.user.is_authenticated:  # of address field was attempted
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
