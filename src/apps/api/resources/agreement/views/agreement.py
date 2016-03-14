import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.conf import settings

from src.domain.agreement.commands import UpdateAgreementAttrs, DeleteAgreement
from src.domain.agreement.entities import Agreement
from src.domain.asset import command_handlers as asset_command_handlers
from src.domain.asset.commands import CreateAssetFromFile
from src.domain.potential_agreement import command_handlers as potential_agreement_command_handlers
from src.domain.potential_agreement.commands import CreatePotentialAgreement, CompletePotentialAgreement
from src.domain.common.enums import DurationTypeEnum
from src.apps.agreement_translation.services import agreement_translation_service
from src.apps.realtime.agreement import services as realtime_agreement_service
from src.libs.common_domain import dispatcher, aggregate_repository
from src.libs.datetime_utils import datetime_utils

constants = settings.CONSTANTS

logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def agreement_create_view(request,
                          _agreement_translation_service=None,
                          _asset_command_handler=None,
                          _potential_agreement_command_handler=None,
                          _realtime_agreement_service=None):
  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804

  # this probably requires some type of saga implementation because we're not supposed to persist so many
  # types of aggregates in one tx
  # https://app.asana.com/0/10235149247655/97940309429278

  if not _agreement_translation_service: _agreement_translation_service = agreement_translation_service
  if not _asset_command_handler: _asset_command_handler = asset_command_handlers
  if not _potential_agreement_command_handler: _potential_agreement_command_handler = potential_agreement_command_handlers
  if not _realtime_agreement_service: _realtime_agreement_service = realtime_agreement_service

  try:
    # get file and process it, validate it. capture info, like filename and other metadata.
    # if all goes well, submit to s3.
    contract_files = [file for file_name, file in request.FILES.items() if file_name.startswith('contracts')]

    # do this task first because persisting the asset will alter the file (name, etc.)
    agreement_data = _agreement_translation_service.get_agreement_info_from_files(contract_files)

    assets = [
      _asset_command_handler.create_asset_from_file(**{'command': CreateAssetFromFile(constants.ARTIFACTS_ROOT, file)})
      for file in contract_files
      ]

    asset_ids = [asset.id for asset in assets]

    command = CreatePotentialAgreement(agreement_data[constants.AGREEMENT_NAME], asset_ids, request.user.id)
    pa = _potential_agreement_command_handler.create_potential_agreement(**{'command': command})
    pa_data = {'id': pa.id}

    # https://app.asana.com/0/10235149247655/97984861912448
    _realtime_agreement_service.save_agreement_edit_in_firebase(pa.id, name=command.name, user_id=command.user_id)

  except Exception as e:
    logger.warn("Error creating agreement: {0}".format(request.data), exc_info=True)
    response = Response("Error creating agreement %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(pa_data, status.HTTP_201_CREATED)

  return response


@api_view(['PUT', 'DELETE'])
def agreement_modify_view(request, agreement_id):
  if request.method == 'PUT':
    ret_val = _update_agreement_view(request, agreement_id)
  else:
    ret_val = _delete_agreement_view(request, agreement_id)

  return ret_val


def _update_agreement_view(request, agreement_id, _dispatcher=None, _aggregate_repo=None, _datetime_utils=None):
  # refer to https://app.asana.com/0/10235149247655/46440394636647
  if not _dispatcher: _dispatcher = dispatcher
  if not _aggregate_repo: _aggregate_repo = aggregate_repository
  if not _datetime_utils: _datetime_utils = datetime_utils

  try:

    try:
      _aggregate_repo.get(Agreement, agreement_id)
      is_potential_agreement = False
    except ObjectDoesNotExist:
      is_potential_agreement = True

    agreement_type = request.data[constants.TYPE_ID]

    name = request.data[constants.NAME]
    counterparty = request.data[constants.COUNTERPARTY]
    description = request.data[constants.DESCRIPTION]
    execution_date = _datetime_utils.get_utc_from_timestamp(request.data[constants.EXECUTION_DATE])
    term_length_time_amount = request.data[constants.TERM_LENGTH_TIME_AMOUNT]
    term_length_time_type = DurationTypeEnum[request.data[constants.TERM_LENGTH_TIME_TYPE]]
    auto_renew = bool(request.data[constants.AUTO_RENEW])
    outcome_notice_time_amount = request.data[constants.OUTCOME_NOTICE_TIME_AMOUNT]
    outcome_notice_time_type = DurationTypeEnum[request.data[constants.OUTCOME_NOTICE_TIME_TYPE]]
    duration_details = request.data[constants.DURATION_DETAILS]
    outcome_notice_alert_enabled = bool(request.data[constants.OUTCOME_NOTICE_ALERT_ENABLED])
    outcome_notice_alert_time_amount = request.data[constants.OUTCOME_NOTICE_ALERT_TIME_AMOUNT]
    outcome_notice_alert_time_type = DurationTypeEnum[request.data[constants.OUTCOME_NOTICE_ALERT_TIME_TYPE]]
    expiration_alert_enabled = bool(request.data[constants.EXPIRATION_ALERT_ENABLED])
    expiration_alert_time_amount = request.data[constants.EXPIRATION_ALERT_TIME_AMOUNT]
    expiration_alert_time_type = DurationTypeEnum[request.data[constants.EXPIRATION_ALERT_TIME_TYPE]]

    data = {
      'name': name,
      'counterparty': counterparty,
      'description': description,
      'execution_date': execution_date,
      'agreement_type_id': agreement_type,
      'term_length_time_amount': term_length_time_amount,
      'term_length_time_type': term_length_time_type,
      'auto_renew': auto_renew,
      'outcome_notice_time_amount': outcome_notice_time_amount,
      'outcome_notice_time_type': outcome_notice_time_type,
      'duration_details': duration_details,
      'outcome_notice_alert_enabled': outcome_notice_alert_enabled,
      'outcome_notice_alert_time_amount': outcome_notice_alert_time_amount,
      'outcome_notice_alert_time_type': outcome_notice_alert_time_type,
      'expiration_alert_enabled': expiration_alert_enabled,
      'expiration_alert_time_amount': expiration_alert_time_amount,
      'expiration_alert_time_type': expiration_alert_time_type,
    }
    if is_potential_agreement:
      command = CompletePotentialAgreement(**data)
    else:
      command = UpdateAgreementAttrs(**data)

    _dispatcher.send_command(agreement_id, command)

  except Exception as e:
    logger.warn("Error saving agreement: {0}".format(request.data), exc_info=True)
    response = Response("Error saving agreement %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(status=status.HTTP_200_OK)

  return response


def _delete_agreement_view(request, agreement_id, _dispatcher=None, ):
  # this method should be considered internal and no public api call should be allowed to pass in a file for an agreement
  # refer to https://app.asana.com/0/10235149247655/46476660493804
  if not _dispatcher: _dispatcher = dispatcher

  try:
    command = DeleteAgreement()

    _dispatcher.send_command(agreement_id, command)

  except Exception as e:
    logger.warn("Error deleting agreement: {0}".format(request.data), exc_info=True)
    response = Response("Error deleting agreement %s " % e, status.HTTP_400_BAD_REQUEST)

  else:
    response = Response(status=status.HTTP_200_OK)

  return response
