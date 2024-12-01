from django.db import models

class Course(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='course name'
    )
    description = models.TextField(
        verbose_name='description'
    )
    preview = models.ImageField(
        upload_to='courses/preview',
        verbose_name='Course preview'
    )
    changed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Lesson title'
    )
    preview = models.ImageField(
        upload_to='courses/preview',
        verbose_name='Lesson preview'
    )
    video_url = models.URLField(
        blank=True,
        null=True
    )
    changed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Lesson'
        verbose_name_plural='Lessons'

    def __str__(self):
        return self.title
