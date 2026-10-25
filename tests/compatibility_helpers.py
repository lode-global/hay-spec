"""Normalize only explicitly permitted nutrient-definition changes for old guards."""
import copy


def restore_previous_document_metadata(sections, previous_sections):
    result = copy.deepcopy(sections)
    current = next(s for s in result if s['id'] == 'metadata')
    previous = next(s for s in previous_sections if s['id'] == 'metadata')
    old = {s['id']: s for s in previous['subsections']}
    current['subsections'] = [copy.deepcopy(old[s['id']])
                              if s['id'] in {'version_history', 'document_metadata'} else s
                              for s in current['subsections']]
    return result


def restore_previous_release_metadata(spec, previous):
    result = copy.deepcopy(spec)
    for key in ('version', 'published_on'):
        result[key] = previous[key]
    for key in ('prepared_on', 'publication_status'):
        result.pop(key, None)
    result['sections'] = restore_previous_document_metadata(result['sections'], previous['sections'])
    return result


def restore_previous_nutrient_definitions(sections, previous_sections):
    result = copy.deepcopy(sections)
    current = next(s for s in result if s['id'] == 'nutrient_analysis')
    previous = next(s for s in previous_sections if s['id'] == 'nutrient_analysis')
    old_dry = [f for f in previous['fields'] if f['id'] == 'dry_matter']
    new_dry = [f for f in current['fields'] if f['id'] == 'dry_matter']
    moisture = [f for f in current['fields'] if f['id'] == 'moisture_content']
    if len(old_dry) != 2 or len(new_dry) != 1 or len(moisture) != 1:
        raise ValueError('Expected exactly the reviewed duplicate consolidation and moisture addition.')
    retained = {k: v for k, v in new_dry[0].items() if k != 'guidance'}
    if retained != old_dry[1]:
        raise ValueError('The retained dry-matter definition changed beyond additive guidance.')
    if (moisture[0].get('data_type') != 'float'
            or moisture[0].get('required') is not False
            or 'required_if' in moisture[0]
            or moisture[0].get('valid_range') != {'min': 0, 'max': 100}):
        raise ValueError('Moisture no longer matches the reviewed optional percentage contract.')
    first_dry = old_dry[0]
    for i, field in enumerate(current['fields']):
        if field['id'] == 'moisture_content':
            current['fields'][i] = copy.deepcopy(first_dry)
        elif field['id'] == 'dry_matter':
            field.pop('guidance', None)
    return result
