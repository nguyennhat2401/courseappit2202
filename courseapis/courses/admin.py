from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.urls import path
from unicodedata import category

from courses.models import Course, Category, Lesson, Tag

class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id','subject','active','created_date']
    search_fields = ['subject']
    list_filter = ['id', 'created_date']
    list_editable = ['subject']
    readonly_fields = ['image_view']

    def image_view(self, lesson):
        if lesson:
            return mark_safe(f"<img src='/static/{lesson.image.name}' width='200' /")


class CourseAppAdminSite(admin.AdminSite):
    site_header = "Quản lý khóa học"

    def get_urls(self):
        return [path('course-stats', self.course_stats)] + super().get_urls()

    def course_stats(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')).values('id', 'name', 'course_count')
        return TemplateResponse(request, 'admin/stats.html',{
            'stats' : stats
        })

ad_site= CourseAppAdminSite(name='ad_site')

ad_site.register(Category)
ad_site.register(Course)
ad_site.register(Tag)
ad_site.register(Lesson, MyLessonAdmin)
