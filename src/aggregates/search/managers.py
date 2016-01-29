from django.db import models


class UserManager(models.Manager):
  def get_by_natural_key(self, user_id):
    return self.get(user_id=user_id)
