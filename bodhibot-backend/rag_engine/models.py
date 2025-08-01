from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

# Create your models here.

# A model to link all the document uploaded, it's metadata and the user who uploaded it...
class Document(models.Model):
    # Who uploaded it?
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, related_name= "uploaded_documents")
    
    # The actual document:
    document = models.FileField(upload_to= "rag_engine/documents/")
    document_name = models.CharField(max_length= 255)
    
    # Metadata, helpful for filtered searching
    department = models.CharField(max_length= 255)
    tags = ArrayField(
        base_field= models.CharField(max_length= 15), 
        blank= True, 
        default= list
    ) 
    audience = ArrayField(
        base_field= models.CharField(max_length= 15), 
        blank= True, 
        default= list
    )
    confidential = models.BooleanField(default= False) # If true, only included in searching by admin & hr level staff.

    # Timestamp:
    created_at = models.DateTimeField(auto_now_add= True)

    # Celery Specific:
    task_id = models.CharField(max_length= 255, blank= True, null= True, help_text= "Task id returned by celery")
    status = models.CharField(
        max_length= 20,
        choices= [
            ("queued", "Queued"),
            ("processing", "Processing"),
            ("success", "Success"),
            ("failed", "Failed")
        ],
        blank= True,
        default= "queued",
        help_text= "Vectorization Status of the document..."
    )
