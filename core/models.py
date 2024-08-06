from django.db import models

# Create your models here.


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=200) 
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    class Meta:
        verbose_name = "İteşim"
        verbose_name_plural = "İteşim"

    def __str__(self):
        return self.full_name