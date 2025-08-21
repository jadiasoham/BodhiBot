from django.db import models
from users.models import User
from uuid import uuid4

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True)
    # user = models.CharField(max_length= 50, verbose_name= "user name", default= "Anonymous User", help_text= "Identifier for the user, can be a username or any unique identifier, is extracted from the decoded jwt token sent from the frontend.")
    name = models.CharField(max_length= 255)
    room_name = models.UUIDField(unique= True, default= uuid4, editable= False, help_text= "Unique room_name for WS upgrade and also unique identifier for this chat.")
    created_at = models.DateTimeField(auto_now_add= True)
    last_message = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"Chat {self.name} started at {self.created_at}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name= "chat_messages", on_delete= models.CASCADE)
    sender = models.CharField(max_length= 50)
    content = models.TextField(verbose_name= "message")
    timestamp = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Message: {self.content} sent by {self.sender} at {self.timestamp}"


class GatekeeperLogs(models.Model): 
    message = models.ForeignKey(Message, related_name= "message_review", on_delete= models.CASCADE)
    blocked_at = models.CharField(max_length= 30, null= True, blank= True, help_text= "Which layer blocked this message?")
    reason = models.TextField(verbose_name= "reason", help_text= "Why was this query blocked or allowed?")
    reviewed_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        action = "Allowed" if not self.blocked_at else "Blocked"
        return f"{self.message.content} by {self.message.sender} was reviewed and {action}. Reason: {self.reason[:50]}..."
    

class GatekeeperLogReview(models.Model):
    reviewer = models.ForeignKey(User, related_name= "log_review", on_delete= models.SET_NULL, null= True, help_text= "Who reviewed?")
    log = models.OneToOneField(GatekeeperLogs, related_name= "log_review", on_delete= models.CASCADE)
    action_ok = models.BooleanField(help_text= "Was the action (Allow/ Block) appropriate?")
    rating = models.SmallIntegerField(choices=[(i, str(i)) for i in range(5)], help_text= "How good was the reason provided?")
    comment = models.TextField(null= True, blank= True, help_text= "Any additional comments by the reviewer")
    reviewed_at = models.DateTimeField(auto_now_add= True)


class UsagePolicy(models.Model):
    policy = models.JSONField()
    updated_on = models.DateTimeField(auto_now_add= True)
