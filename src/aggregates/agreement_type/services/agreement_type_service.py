from src.aggregates.agreement_type.models import AgreementType
from src.aggregates.agreement_type.services import agreement_type_factory


def save_or_update(agreement_type):
  agreement_type.save(internal=True)


def create_agreement_type(agreement_type_name, agreement_type_global, agreement_type_user_id):
  agreement_type = agreement_type_factory.create_agreement_type(agreement_type_name, agreement_type_global,
                                                                agreement_type_user_id)
  save_or_update(agreement_type)
  return agreement_type


def get_agreement_type(agreement_type_id):
  return AgreementType.objects.filter(agreement_type_id=agreement_type_id)


def get_global_agreement_types():
  return AgreementType.objects.filter(agreement_type_global=True)
