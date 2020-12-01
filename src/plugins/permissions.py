from store.models import Store, Product, Plugin, 
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
codename='can_publish',
name='Can Publish Posts',
content_type=content_type,
)