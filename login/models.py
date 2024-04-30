from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    # this can be changed by a Django admin, everyone defaulted to False for being a site admin
    is_admin = models.BooleanField(default=False)
    # adding in this email field, so we can check the email from Google and grab the registered user associated
    # with this email (to see if they're an admin)
    email = models.EmailField(max_length = 254, blank=True,unique=True)
    username = models.CharField(max_length = 150)
    #later add in a foreign key reference to reports, so a user's reports are stored

    def __str__(self):
        return self.username

    def get_reports(self):
        # purpose: since foreign key isn't working well for anonymous reports...
        # when you are trying to load a user's reports, see which reports' usernames match this username
        reports = Report.objects.filter(username__exact=self.username)
        if reports.count() == 0:
            return None
        else:
            return reports


# COMMENTING OUT FOR POSSIBLE LATER USE - Joe
# class Report (models.Model):
    # # an admin marks a report as resolved, maybe with a checkbox
    # resolved = models.BooleanField(default=False)
    # # this is the user that submitted the report (TODO how to represent this is anonymous)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    # # this is a placeholder, we will need to add more fields
    # #problem_text = models.CharField(max_length = 400)

    # # need to add more form fields, file savers?

    # def __str__(self):
    #     if self.user:
    #         return "Report " + str(self.id) + "- user: " + self.user.username + ", resolved: " + str(self.resolved)
    #     else:
    #         return "Report " + str(self.id) + "- (anonymous), resolved: " + str(self.resolved)

class Report(models.Model):

    ## Megan added - from OG model
    username = models.CharField(max_length=150, default="(anonymous)")
    resolved = models.BooleanField(default=False)
    notes = models.TextField(default='', blank=True, verbose_name = "Administrator Notes")

    # from form
    full_name = models.CharField(max_length=200, default = '')
    incident_type = models.CharField(max_length=50, default = '')
    description = models.TextField(default = '', blank = True)
    location = models.CharField(max_length=500, default = '', blank = True)
    images = models.ImageField(upload_to='report_images/', default = '', blank = True)
    videos = models.FileField(upload_to='report_videos/', default = '', blank = True)
    submission_date = models.DateTimeField(default = timezone.now)

    #Statuses
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    def __str__(self):
        incident_selection = ""
        if self.incident_type == "1":
            incident_selection = "Security Breach"
        elif self.incident_type == "2":
            incident_selection = "Physical Altercation"
        elif self.incident_type == "3":
            incident_selection = "Theft or Vandalism"
        elif self.incident_type == "4":
            incident_selection = "Harassment or Discrimination"
        elif self.incident_type == "5":
            incident_selection = "Accident or Injury"
        elif self.incident_type == "6":
            incident_selection = "Medical Emergency"
        elif self.incident_type == "7":
            incident_selection = "Fire or Hazardous Materials Incident"
        elif self.incident_type == "8":
            "Cybersecurity Incident"
        elif self.incident_type == "9":
            incident_selection = "Missing Person"
        else:
            incident_selection = "Suspicious Activity"
        return incident_selection + ", location: " + self.location

