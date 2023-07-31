# department/todo_app/views.py
from django.urls import reverse, reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import ToDoItem, ToDoList

from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from matplotlib.ticker import MaxNLocator

def uri():
    departments = []
    counts = []
    for department in ToDoList.objects.all():
        departments.append(department.title)
        counts.append(department.todoitem_set.count())
    
    fig, ax = plt.subplots(figsize =(16, 9))

    # Horizontal Bar Plot
    ax.barh(departments, counts)
    
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    # Show top values
    ax.invert_yaxis()

    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')
    
    # Add Plot Title
    ax.set_title('Texts added in different categories',
                loc ='left', )

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)

class PlotView(ListView):
    model = ToDoList
    template_name = "todo_app/plot_report.html"

    def get_context_data(self,**kwargs):
        context = dict()
        context['data'] = uri()
        return context

class AuthorsListView(ListView):
    model = ToDoItem
    template_name = "todo_app/authors_report.html"

    def get_queryset(self):
        res = ToDoItem.objects.none()
        seen = set()
        for item in ToDoItem.objects.all().iterator():
            if item.author.upper() not in seen:
                seen.add(item.author.upper())
                res |= ToDoItem.objects.filter(pk=item.pk)
        return res

    def get_context_data(self,**kwargs):
        context = super(AuthorsListView,self).get_context_data(**kwargs)
        return context

class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_context_data(self,**kwargs):
        context = super(ListListView,self).get_context_data(**kwargs)
        return context


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(department_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["department"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class AuthorListView(ListView):
    model = ToDoItem
    template_name = "todo_app/author.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(author__iexact=self.kwargs["author"])

    def get_context_data(self):
        context = super().get_context_data()
        context["author_name"] = self.kwargs["author"]
        context["len"] = ToDoItem.objects.filter(author__iexact=self.kwargs["author"]).count()
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new department"
        return context


class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "department",
        "title",
        "author",
        "description",
        "start_date",
        "due_date",
        "status",
        "category",
        "score"
    ]

    def get_initial(self):
        initial_data = super().get_initial()
        department = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["department"] = department
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        department = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["department"] = department
        context["title"] = "Add a new text"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.department_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "department",
        "title",
        "author",
        "description",
        "start_date",
        "due_date",
        "status",
        "category",
        "score"
    ]

    def get_context_data(self):
        context = super().get_context_data()
        context["department"] = self.object.department
        context["title"] = "Edit text"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.department_id])


class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department"] = self.object.department
        return context
