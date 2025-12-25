from django.db import models


#############################################
# Models for Reddit API Data Storage #
#############################################


class CustomFeed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ApiRedditPost(models.Model):
    post_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique Reddit post identifier",
    )
    subreddit = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    selftext = models.TextField(blank=True, null=True)
    score = models.IntegerField()
    upvote_ratio = models.FloatField()
    author = models.CharField(max_length=100)
    url = models.URLField()
    num_comments = models.IntegerField()
    permalink = models.URLField()
    over_18 = models.BooleanField(default=False)
    is_self = models.BooleanField(default=False)
    created_utc = models.DateTimeField()

    # domain = models.CharField(max_length=100)
    video_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)

    custom_feeds = models.ManyToManyField(
        CustomFeed,
        related_name="reddit_posts",
        blank=True,
    )

    favorite = models.BooleanField(default=False)

    # AI Response fields
    ai_response = models.TextField(
        blank=True, null=True, help_text="AI generated response from OpenRouter"
    )
    ai_response_created_at = models.DateTimeField(
        blank=True, null=True, help_text="Timestamp when AI response was generated"
    )
    ai_model_used = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="AI model used to generate the response",
    )

    def __str__(self):
        return self.title[:15] + "..." if len(self.title) > 30 else self.title


class ApiRedditComment(models.Model):
    post = models.ForeignKey(
        ApiRedditPost, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    score = models.IntegerField()
    created_utc = models.DateTimeField(null=True, blank=True)
    # author = models.CharField(max_length=100)
    # subreddit = models.CharField(max_length=100)

    def __str__(self):
        return f"Comment by {self.post}"
