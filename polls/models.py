from django.db import models
from django.utils import timezone

class Tournament(models.Model):
    tournament_name = models.CharField(max_length=200, default=None, null=True, blank=True)
    user_id = models.CharField(max_length=200, default=None, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.tournament_name

class Level(models.Model):
    level_name =  models.CharField(max_length=200)
    tournament_id = models.ForeignKey(Tournament, default=None, null=True, blank=True, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2083, blank=True)
    negative_marking = models.IntegerField()
    def __str__(self):
        return self.level_name
    

TEAMIMAGES = (
    ("https://cms-assets.tutsplus.com/uploads/users/346/posts/31688/image/sportslogos16.jpg","Bulls"),
    ("https://cmkt-image-prd.global.ssl.fastly.net/0.1.0/ps/5942957/300/200/m1/fpnw/wm0/mockuppanda-.jpg?1551077845&s=2efd525056f579874e9030216c4d7c9c","Panda"),
    ("https://designrshub-designrshub.netdna-ssl.com/wp-content/uploads/2019/01/sports-animal-mascot-logo-design-ideas-08.jpg","Shark"),
    ("https://designrshub-designrshub.netdna-ssl.com/wp-content/uploads/2019/01/sports-animal-mascot-logo-design-ideas-13.jpg","Deer"),
    ("https://cdn2.vectorstock.com/i/1000x1000/34/31/wild-wolf-esport-mascot-logo-design-vector-27463431.jpg","Wolf"),
    ("https://designrshub-designrshub.netdna-ssl.com/wp-content/uploads/2019/01/sports-animal-mascot-logo-design-ideas-18.jpg","Fox")
)
class Team(models.Model):
    tournament_id = models.ForeignKey(Tournament, default=None, null=True, blank=True, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=2083)
    team_points = models.IntegerField(default=0)
    images = models.CharField(
        max_length=2000,
        choices=TEAMIMAGES,
        default=None,
        blank = True,
        null = True,
    )

class Category(models.Model):
    tournament_id = models.ForeignKey(Tournament, default=None, null=True, blank=True, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=2083)
    image_url = models.CharField(max_length=2083, blank=True, default="http://via.placeholder.com/72")
    def __str__(self):
        return self.category_name

CHOICES = (
    ("NA","Not Answered"),
    ("PQ","Passed Question"),
    ("RA","Right Answer"),
    ("WA","Wrong Answer")
)
class Question(models.Model):
    tournament_id = models.ForeignKey(Tournament, default=None, null=True, blank=True, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=5000)
    question_number = models.IntegerField()
    image_url = models.CharField(max_length=2083, blank=True)
    marks_alloted = models.IntegerField()
    time_alloted = models.IntegerField(default=60)
    team_choose = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True, blank=True)
    pass_count = models.IntegerField()
    status = models.CharField(
        max_length=2,
        choices=CHOICES,
    default="NA",
    )
    answer = models.CharField(max_length=5000)
    def __str__(self):
        return self.question_text
    class Meta:
        ordering = ['marks_alloted']
