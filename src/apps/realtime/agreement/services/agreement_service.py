from src.aggregates.potential_agreement.services import potential_agreement_service
from src.apps.agreement.enums import DurationTypeEnum, AgreementTypeEnum
from src.libs.firebase_utils.services import firebase_provider


def save_agreement_edit_in_firebase(potential_agreement_id, _potential_agreement_service=None, _firebase_provider=None):
  if not _potential_agreement_service: _potential_agreement_service = potential_agreement_service
  if not _firebase_provider: _firebase_provider = firebase_provider

  client = _firebase_provider.get_firebase_client()

  potential_agreement = _potential_agreement_service.get_potential_agreement(potential_agreement_id)

  # http://stackoverflow.com/questions/14524322/how-to-convert-a-date-string-to-different-format
  if potential_agreement.potential_agreement_execution_date:
    execution_date = potential_agreement.potential_agreement_execution_date.strftime('%Y-%m-%d')
  else:
    execution_date = None

  if potential_agreement.potential_agreement_renewal_notice_type:
    renewal_notice_type = DurationTypeEnum(potential_agreement.potential_agreement_renewal_notice_type).name
  else:
    renewal_notice_type = None

  if potential_agreement.potential_agreement_term_length_amount:
    term_length_type = DurationTypeEnum(potential_agreement.potential_agreement_term_length_amount).name
  else:
    term_length_type = None

  if potential_agreement.potential_agreement_type:
    agreement_type = AgreementTypeEnum(potential_agreement.potential_agreement_type).name
  else:
    agreement_type = None

  data = {
    'auto-renew': potential_agreement.potential_agreement_auto_renew,
    'counterparty': potential_agreement.potential_agreement_counterparty,
    'description': potential_agreement.potential_agreement_description,
    'duration-details': potential_agreement.potential_agreement_duration_details,
    'execution-date': execution_date,
    'name': potential_agreement.potential_agreement_name,
    'renewal-notice-amount': potential_agreement.potential_agreement_renewal_notice_amount,
    'renewal-notice-type': renewal_notice_type,
    'term-length-amount': potential_agreement.potential_agreement_term_length_amount,
    'term-length-type': term_length_type,
    'type': agreement_type,
    'viewers': {potential_agreement.potential_agreement_user_id: True}
  }

  result = client.put('/agreement-edits', potential_agreement_id, data)

  return result
