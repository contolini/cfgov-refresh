from django.conf import settings


DEFAULT_REGULATIONS_REFERENCE_MAPPING = [
    (
        r'(?P<section>[\w]+)-(?P<paragraph>[\w-]*)',
        '{section}',
        '{paragraph}'
    ),
]
REGULATIONS_REFERENCE_MAPPING = getattr(
    settings,
    'REGULATIONS_REFERENCE_MAPPING',
    DEFAULT_REGULATIONS_REFERENCE_MAPPING
)
