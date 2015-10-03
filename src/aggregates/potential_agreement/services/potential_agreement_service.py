from src.aggregates.potential_agreement.services import potential_agreement_factory


def save_or_update(agreement):
  agreement.save(internal=True)


def create_potential_agreement(potential_agreement_name, potential_agreement_artifacts):
  agreement = potential_agreement_factory.create_potential_agreement(potential_agreement_name,
                                                                     potential_agreement_artifacts)
  save_or_update(agreement)
  return agreement
