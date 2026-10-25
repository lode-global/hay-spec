"""Normalize only explicitly permitted nutrient-definition changes for old guards."""
import copy


def restore_previous_nutrient_definitions(sections, previous_sections):
    result = copy.deepcopy(sections)
    current = next(s for s in result if s['id'] == 'nutrient_analysis')
    previous = next(s for s in previous_sections if s['id'] == 'nutrient_analysis')
    first_dry = next(f for f in previous['fields'] if f['id'] == 'dry_matter')
    for i, field in enumerate(current['fields']):
        if field['id'] == 'moisture_content':
            current['fields'][i] = copy.deepcopy(first_dry)
        elif field['id'] == 'dry_matter':
            field.pop('guidance', None)
    return result
