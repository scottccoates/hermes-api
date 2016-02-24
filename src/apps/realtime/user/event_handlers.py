from django.dispatch import receiver

from src.aggregates.user.signals import created
from src.apps.realtime.user.services import user_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def user_created_callback(**kwargs):
  user_id = kwargs.pop('id')
  name = kwargs.pop('name')
  nickname = kwargs.pop('nickname')
  email = kwargs.pop('email')
  picture = kwargs.pop('picture')

  user_tasks.save_user_info_in_firebase_task.delay(
    user_id, name, nickname,
    email, picture
  )
