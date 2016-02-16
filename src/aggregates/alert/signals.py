from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['user_name', 'user_nickname', 'user_email', 'user_picture', 'user_attrs', 'user_system_created_date']
)
updated_attrs = EventSignal(
  'updated_attrs', __name__, 1,
  providing_args=['alert_id', 'alert_name', 'alert_query']
)
