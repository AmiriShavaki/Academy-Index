# department/todo_app/models.py
from django.utils import timezone

from django.db import models
from django.urls import reverse


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    STATUS_CHOICES = (
        ('w', 'Writing'),
        ('e', 'Editing'),
        ('l', 'Linkedin'),
        ('j', 'Journal'),
        ('i', 'Linkedin & Journal')
    )

    CATEGORY_CHOICES = (
        ('n', 'Nanotechnology & Drug Delivery'),
        ('g', 'Gene Therapy & Genetic Medicine'),
        ('i', 'Infectious Disease and Microbiology'),
        ('r', 'RNA Therapeutics and RNA Technology'),
        ('u', 'Nucleic Acid Chemistry'),
        ('m', 'Immunotherapy and Immunology'),
        ('a', 'Manufacturing Technology'),
        ('o', 'Others')
    )

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=one_week_hence)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    department = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    score = models.PositiveSmallIntegerField(null=True)
    author = models.CharField(max_length=100)
    author_cnt = models.PositiveSmallIntegerField(default=0)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.department.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["created_date"]
