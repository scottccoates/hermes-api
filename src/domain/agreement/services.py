from django.utils import timezone

from src.domain.agreement.models import AgreementSearch, AgreementAlert


def get_agreements_with_due_expiration_alert():
  ret_val = AgreementAlert.objects.filter(
    expiration_alert_date__lte=timezone.now(),
    expiration_alert_enabled=True,
    expiration_alert_created=False
  )
  return ret_val


def get_agreements_with_due_outcome_notice_alert():
  ret_val = AgreementAlert.objects.filter(
    outcome_notice_alert_date__lte=timezone.now(),
    outcome_notice_alert_enabled=True,
    outcome_notice_alert_created=False
  )
  return ret_val


def get_agreement_search(agreement_id):
  ag = AgreementSearch.objects.get(id=agreement_id)
  return ag


def save_agreement_search(agreement_id, user_id, name, counterparty, agreement_type_id):
  ag, _ = AgreementSearch.objects.update_or_create(
    id=agreement_id, defaults=dict(
      name=name, user_id=user_id, counterparty=counterparty, agreement_type_id=agreement_type_id
    )
  )
  return ag


def get_agreement_alert(agreement_id):
  ag = AgreementAlert.objects.get(id=agreement_id)
  return ag


def save_agreement_alert(agreement_id,
                         outcome_notice_alert_date, outcome_notice_alert_enabled, outcome_notice_alert_created,
                         expiration_alert_date, expiration_alert_enabled, expiration_alert_created, ):
  data = {
    'outcome_notice_alert_date': outcome_notice_alert_date,
    'outcome_notice_alert_enabled': outcome_notice_alert_enabled,
    'outcome_notice_alert_created': outcome_notice_alert_created,
    'expiration_alert_date': expiration_alert_date,
    'expiration_alert_enabled': expiration_alert_enabled,
    'expiration_alert_created': expiration_alert_created,
  }

  obj, _ = AgreementAlert.objects.update_or_create(id=agreement_id, defaults=data)

  return obj


def delete_agreementsearch(agreement_id):
  get_agreement_alert(agreement_id).delete()
  get_agreement_search(agreement_id).delete()
