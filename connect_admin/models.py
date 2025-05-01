from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        choices=(
            ('ongoing', 'Ongoing'),
            ('upcoming', 'Upcoming'),
            ('completed', 'Completed'),
        ), 
        max_length=100
    )
    type = models.CharField(
        choices=(
            ('health', 'Health'), 
            ('education', 'Education'), 
            ('other', 'Other')
        ), 
        max_length=100
    )   
    location = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.project.name}"

    def save(self, *args, **kwargs):
        # Ensure only one main image exists per project
        if self.is_main:
            ProjectImage.objects.filter(project=self.project, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )

    def __str__(self):
        return f"{self.name} - {self.rating or 'No'} stars"

    def get_stars(self):
        """Returns HTML for star rating display"""
        if not self.rating:
            return ""
        full_stars = self.rating
        empty_stars = 5 - full_stars
        stars = ['<i class="fas fa-star text-warning"></i>'] * full_stars
        stars += ['<i class="far fa-star text-warning"></i>'] * empty_stars
        return mark_safe("".join(stars))
    

class Member(models.Model):
    member_id = models.CharField(max_length=8, unique=True, editable=False)
    name = models.CharField(max_length=200)
    gender = models.CharField(
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female')
        ), max_length=100
    )
    type = models.CharField(
        choices=(
            ('executive', 'Executive'),
            ('member', 'Member')
        ), max_length=100
    )
    position = models.CharField(
        choices=(
            ('president', 'President'),
            ('vice_president', 'Vice President'),
            ('secretary', 'Secretary'),
            ('treasurer', 'Treasurer'),
            ('member', 'Member')
        ), max_length=100, default='member'
    )
    status = models.CharField(
        choices=(
            ('pending', 'pending'),
            ('accepted', 'accepted'),
            ('declined', 'declined'),
        ), max_length=100, default='accepted'
    )
    picture = models.ImageField(upload_to='members/')
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.member_id:
            # Ensure only numeric member IDs are used
            last_member = Member.objects.exclude(member_id__isnull=True).exclude(member_id__exact='').order_by('id').last()
            
            # Get the next numeric ID, default to 1 if no valid member_id exists
            if last_member and last_member.member_id.isdigit():
                next_id = int(last_member.member_id) + 1
            else:
                next_id = 1

            # Pad the numeric ID to 8 characters
            self.member_id = str(next_id).zfill(8)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Scholarship(models.Model):
    name = models.CharField(max_length=500)
    type = models.CharField(choices=(
        ('local', 'Local'),
        ('foreign', 'Foreign')
    ), max_length=100)  
    amount = models.IntegerField()
    description = models.TextField()
    recipient_name = models.CharField(max_length=200)
    recipient_id_number = models.CharField(max_length=20, unique=True)
    recipient_email = models.EmailField(max_length=200)
    recipient_phone = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient_name + ' - ' + self.type