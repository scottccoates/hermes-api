from src.domain.user.models import AuthUser


def create_auth_user(id, email, system_created_date):
  user = AuthUser(id=id, email=email, system_created_date=system_created_date)
  user.save()
  return user


def get_auth_user_from_email(email):
  return AuthUser.objects.get(email=email)
