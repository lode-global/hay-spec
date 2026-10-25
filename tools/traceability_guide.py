"""Build read-only section guides without changing canonical definitions."""
import json
from pathlib import Path


EXAMPLES = {
    'hay_single_lot_traceable': 'hay_single_lot_traceable: true',
    'lot_identifier_internal': 'lot_identifier_internal: LOT-042',
    'lot_identifier_external': ('lot_identifier_external:\n'
                                '  lot_identifier_external.value: "00017-A"\n'
                                '  lot_identifier_external.issuer: USDA'),
    'lot_mapping_field_to_bale_supported': 'lot_mapping_field_to_bale_supported: false',
    'source_fields': ('source_fields:\n  - field_name: North meadow\n'
                      '    field_identifier: "00017"\n'
                      '    field_identifier_scope: Example Farm / field register\n'
                      '  - field_name: South meadow'),
}
RELATED = {
    'hay_single_lot_traceable': ['source_fields', 'lot_identifier_internal'],
    'lot_identifier_internal': ['lot_identifier_external'],
    'lot_identifier_external': ['lot_identifier_internal'],
    'lot_mapping_field_to_bale_supported': ['source_fields'],
    'source_fields': ['hay_single_lot_traceable', 'lot_mapping_field_to_bale_supported'],
    'field_identifier': ['source_fields/field_identifier_scope', 'source_fields'],
    'field_identifier_scope': ['source_fields/field_identifier', 'source_fields'],
    'field_name': ['source_fields'],
    'lot_identifier_external.value': ['lot_identifier_external/lot_identifier_external.issuer'],
    'lot_identifier_external.issuer': ['lot_identifier_external/lot_identifier_external.value'],
}


NUTRIENT_EXAMPLES = {
    'lab_sample_id': 'lab_sample_id: "00017-A"',
    'moisture_content': 'moisture_content: 12.0',
    'dry_matter': 'dry_matter: 88.0',
    'crude_protein': 'crude_protein: 18.5',
    'soluble_protein_%_cp': 'soluble_protein_%_cp: 25.0',
    'degradable_protein_%_cp': 'degradable_protein_%_cp: 65.0',
}
NUTRIENT_RELATED = {
    'hay_tested': ['hay_testing_laboratory', 'lab_sample_id'],
    'hay_testing_laboratory': ['lab_sample_id', 'lab_report_reference', 'hay_testing_method'],
    'lab_sample_id': ['hay_testing_laboratory', 'lab_report_reference'],
    'lab_report_reference': ['lab_sample_id', 'hay_testing_date'],
    'hay_sample_date': ['hay_testing_date', 'lab_processing_completed_date'],
    'hay_testing_date': ['hay_sample_date', 'lab_processing_completed_date'],
    'lab_processing_completed_date': ['hay_sample_date', 'hay_testing_date'],
    'moisture_content': ['dry_matter'],
    'dry_matter': ['moisture_content'],
    'crude_protein': ['soluble_protein_%_cp', 'degradable_protein_%_cp'],
    'soluble_protein_%_cp': ['crude_protein', 'degradable_protein_%_cp'],
    'degradable_protein_%_cp': ['crude_protein', 'soluble_protein_%_cp'],
}


def guide(spec, display=None, section_id='traceability'):
    """Return None for absent sections; all grouping is presentation-only."""
    indexed = [(i, s) for i, s in enumerate(spec['sections']) if s['id'] == section_id]
    if not indexed:
        return None
    section_index, section = indexed[0]
    titles = (display or {}).get('titles', {})
    examples = NUTRIENT_EXAMPLES if section_id == 'nutrient_analysis' else EXAMPLES
    related = NUTRIENT_RELATED if section_id == 'nutrient_analysis' else RELATED

    def node(item, scope, anchor):
        identity = item.get('id', item.get('name'))
        key = '/'.join([*scope, identity])
        result = {
            'key': key, 'id': identity,
            'title': item.get('title', titles.get(key, identity)),
            'anchor': anchor, 'source': item,
            'example': examples.get(identity),
            'related': [section_id + '/' + value for value in related.get(identity, [])],
            'children': [],
        }
        for collection in ('fields', 'components', 'groups', 'subsections'):
            for index, child in enumerate(item.get(collection, [])):
                result['children'].append(node(child, [*scope, identity],
                                               f'{anchor}-{collection}-{index}'))
        return result

    root = node(section, [], f'node-sections-{section_index}')
    nutrient = section_id == 'nutrient_analysis'
    if nutrient:
        # Slice the visual outline only. Real node keys/anchors and root.source
        # retain the original flat fields, including section-marker definitions.
        groups = (display or {}).get('nutrient_groups', [])
        flat = root['children']
        ids = [item['id'] for item in flat]
        if groups:
            grouped = []
            for index, group in enumerate(groups):
                start = ids.index(group['starts_at'])
                end = ids.index(groups[index + 1]['starts_at']) if index + 1 < len(groups) else len(flat)
                grouped.append({
                    'key': f'navigation/{section_id}/{group["anchor"]}',
                    'title': group['title'], 'id': None, 'presentation': True,
                    'source': {'definition': 'A navigation group for related source fields. '
                               'It introduces no record container, field identifier, or new constraint.'},
                    'children': flat[start:end], 'related': [], 'example': None,
                    'anchor': f'nav-{group["anchor"]}',
                })
            root['children'] = grouped
    data = {
        'version': spec['version'], 'publication': spec.get('publication_status'),
        'root': root, 'sectionId': section_id, 'nutrient': nutrient,
        'reference': f'../fields/{section_id}/',
        'introCard': ('Choose a navigation group, then a laboratory or nutrient field. '
                      'Grouping is visual only: nutrient fields retain their existing flat identifiers.'
                      if nutrient else 'Choose a field from the outline. Expand a component to see its '
                      'members. Source fields is a repeated collection; its members describe each individual entry.'),
        'notice': ('Read each definition for units, reporting basis, and sample context. '
                   'Typical ranges in prose are not hard rejection limits. This guide does not '
                   'convert units, calculate values, or judge feeding suitability.' if nutrient else None),
    }
    # This is JSON inside a script element: prevent source text ending the element.
    payload = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    template = (Path(__file__).parent / 'templates' / 'field-guide.html').read_text()
    from html import escape
    title = section.get('title', section_id)
    intro = ('Explore laboratory provenance, sample basis, and nutrient measurements. '
             'Browse a navigation group or search for an exact field identifier.' if nutrient else
             'Understand how a hay lot connects to its identifiers and contributing production fields. '
             'Explore the outline, then read a field in context.')
    return (template.replace('__SECTION_TITLE__', escape(title))
            .replace('__SECTION_INTRO__', escape(intro))
            .replace('__REFERENCE__', f'../fields/{section_id}/')
            .replace('__GUIDE_DATA__', payload))
