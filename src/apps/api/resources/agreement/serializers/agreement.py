from rest_framework import serializers
from src.aggregates.potential_agreement.models import PotentialAgreement


class PotentialAgreementSerializer(serializers.ModelSerializer):
  class Meta:
    model = PotentialAgreement
    fields = ('id', 'name')
