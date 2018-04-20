import re

from regulations3k.models import Section
from regulations3k import settings
from regulations3k.regdown import extract_labeled_paragraph


def resolve_reference(reference):
    """ Given a reference, return destination section and paragraph labels
    This function uses the REGULATIONS_REFERENCE_MAPPING setting to resolve
    references into their destination section and paragraph labels. It does
    not containing that reference """
    reference_mapping = settings.REGULATIONS_REFERENCE_MAPPING

    for reference_map in reference_mapping:
        reference_re = re.compile(reference_map[0])
        match = reference_re.match(reference)
        if match:
            match_section = match.group('section')
            match_paragraph = match.group('paragraph')
            dest_section_label = reference_map[1].format(section=match_section)
            dest_paragraph_label = reference_map[2].format(
                section=match_section, paragraph=match_paragraph)
            return (dest_section_label, dest_paragraph_label)

    return None, None


def get_contents_resolver(section):
    """ Return a Regdown contents_resolver function to call from the section
    This constructs a contents_resolver that will resolve references and
    return their contents for all sections that are part of the same
    EffectiveVersion as the given section. """
    section_query = Section.objects.filter(
        subpart__version=section.subpart.version,
    )
    def contents_resolver(reference):
        dest_section_label, dest_paragraph_label = resolve_reference(reference)
        try:
            dest_section = section_query.get(label=dest_section_label)
        except Section.DoesNotExist:
            return ''
        dest_paragraph = extract_labeled_paragraph(
            dest_paragraph_label, dest_section.contents)
        return dest_paragraph

    return contents_resolver
