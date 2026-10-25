"""Build a read-only guide from canonical Traceability definitions."""
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


def guide(spec, display=None):
    """Return None for fixtures without Traceability; never rewrite the source."""
    indexed = [(i, s) for i, s in enumerate(spec['sections']) if s['id'] == 'traceability']
    if not indexed:
        return None
    section_index, section = indexed[0]
    titles = (display or {}).get('titles', {})

    def node(item, scope, anchor):
        identity = item.get('id', item.get('name'))
        key = '/'.join([*scope, identity])
        result = {
            'key': key, 'id': identity,
            'title': item.get('title', titles.get(key, identity)),
            'anchor': anchor, 'source': item,
            'example': EXAMPLES.get(identity),
            'related': ['traceability/' + value for value in RELATED.get(identity, [])],
            'children': [],
        }
        for collection in ('fields', 'components', 'groups', 'subsections'):
            for index, child in enumerate(item.get(collection, [])):
                result['children'].append(node(child, [*scope, identity],
                                               f'{anchor}-{collection}-{index}'))
        return result

    data = {'version': spec['version'], 'publication': spec.get('publication_status'),
            'root': node(section, [], f'node-sections-{section_index}')}
    # This is JSON inside a script element: prevent source text ending the element.
    payload = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    template = (Path(__file__).parent / 'templates' / 'traceability-guide.html').read_text()
    return template.replace('__GUIDE_DATA__', payload)
