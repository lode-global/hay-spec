"""Build read-only section guides without changing canonical definitions."""
import json
import re
from html import escape
from pathlib import Path


EXAMPLES = {
    'hay_single_lot_traceable': 'hay_single_lot_traceable: true',
    'lot_identifier_internal': 'lot_identifier_internal: LOT-042',
    'lot_identifier_external': ('lot_identifier_external:\n'
                                '  lot_identifier_external.value: "00017-A"\n'
                                '  lot_identifier_external.issuer: USDA'),
    'lot_mapping_field_to_bale_supported': 'lot_mapping_field_to_bale_supported: false',
    'source_fields_completeness': ('source_fields:\n  - field_name: North meadow\n'
                                   'source_fields_completeness: complete'),
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
    'source_fields': ['hay_single_lot_traceable', 'lot_mapping_field_to_bale_supported', 'source_fields_completeness'],
    'source_fields_completeness': ['source_fields'],
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


SECTION_EXAMPLES = {
    'stand': {'stand_mixture_intended': 'stand_mixture_intended: true',
              'forage_variety_count': 'forage_variety_count: 1'},
    'soil': {'soil_test_ph': 'soil_test_ph: 6.5'},
    'crop_management': {'growth_conditions_notes': 'growth_conditions_notes: Source reported dry conditions.'},
    'harvest': {'bale_count': 'bale_count: 100'},
    'packaging': {'hay_packaging_history': 'hay_packaging_history: original',
                  'bale_dimension_units': 'bale_dimension_units: inches'},
}
SECTION_RELATED = {
    'stand': {
        'forage_variety_count': ['stand_mixture_intended', 'forage_variety_components'],
        'forage_variety_components': ['forage_variety_count', 'stand_mixture_intended'],
        'variety_representation_target': ['forage_variety_components/variety_representation_result'],
        'variety_representation_result': ['forage_variety_components/variety_representation_target'],
    },
    'location': {
        'source_field_area': ['source_field_area_units'],
        'source_field_area_units': ['source_field_area'],
        'source_field_elevation': ['source_field_elevation_units'],
        'source_field_elevation_units': ['source_field_elevation'],
        'irrigation_method_used': ['irrigation_status', 'irrigation_method_available'],
    },
    'soil': {
        'amount_fertilized_nitrogen': ['amount_fertilized_units', 'date_fertilized_nitrogen'],
        'amount_fertilized_potassium': ['amount_fertilized_units', 'date_fertilized_potassium'],
        'amount_fertilized_phosphorus': ['amount_fertilized_units', 'date_fertilized_phosphorus'],
        'amendment_amount': ['organic_amendments_applied/amendment_amount_units'],
        'amendment_amount_units': ['organic_amendments_applied/amendment_amount'],
    },
    'harvest': {
        'source_field_yield': ['source_field_yield_units'],
        'source_field_yield_units': ['source_field_yield'],
        'average_bale_weight': ['bale_weight_assessment_method', 'bale_weight_intended'],
    },
    'packaging': {
        'bale_shape': ['bale_dimension_diameter', 'bale_dimension_axis', 'bale_dimension_height'],
        'bale_dimension_diameter': ['bale_shape', 'bale_dimension_axis', 'bale_dimension_units'],
        'bale_dimension_axis': ['bale_shape', 'bale_dimension_diameter', 'bale_dimension_units'],
        'bale_dimension_height': ['bale_shape', 'bale_dimension_units'],
        'bale_dimension_width': ['bale_shape', 'bale_dimension_units'],
        'bale_dimension_length': ['bale_shape', 'bale_dimension_units'],
        'bale_weight_intended_repackaged': ['hay_packaging_history', 'bale_weight_units'],
    },
    'physical_characteristics': {
        'handling_events': ['final_storage_structure', 'restacked_since_baling'],
        'final_storage_structure': ['handling_events'],
        'stage_label': ['handling_events'],
        'restacked_since_baling': ['handling_events'],
    },
}


def guide(spec, display=None, section_id='traceability'):
    """Return None for absent sections; all grouping is presentation-only."""
    indexed = [(i, s) for i, s in enumerate(spec['sections']) if s['id'] == section_id]
    if not indexed:
        return None
    section_index, section = indexed[0]
    titles = (display or {}).get('titles', {})
    examples = (NUTRIENT_EXAMPLES if section_id == 'nutrient_analysis' else
                EXAMPLES if section_id == 'traceability' else SECTION_EXAMPLES.get(section_id, {}))
    related = (NUTRIENT_RELATED if section_id == 'nutrient_analysis' else
               RELATED if section_id == 'traceability' else SECTION_RELATED.get(section_id, {}))

    def node(item, scope, anchor):
        identity = item.get('id', item.get('name'))
        key = '/'.join([*scope, identity])
        result = {
            'key': key, 'id': identity,
            'title': item.get('title', titles.get(key, identity)),
            'anchor': anchor, 'source': item,
            'example': examples.get(identity),
            'documentary': section_id == 'metadata',
            'legacyStorageEnumGuidance': section_id == 'physical_characteristics' and identity in (
                'final_storage_structure', 'final_surface_type', 'final_airflow_condition',
                'restacked_since_baling', 'visible_moisture_damage'),
            'legacyIdentifierGuidance': key in (
                'traceability/lot_identifier_external',
                'traceability/lot_identifier_external/lot_identifier_external.value',
                'traceability/lot_identifier_external/lot_identifier_external.issuer',
                'nutrient_analysis/soluble_protein_%_cp',
                'nutrient_analysis/degradable_protein_%_cp'),
            'referenceDataGuidance': key in (
                'stand/forage_variety_components/forage_variety',
                'nutrient_analysis/hay_testing_laboratory'),
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
        'metadata': section_id == 'metadata',
        'reference': f'../fields/{section_id}/',
        'introCard': ('Choose a navigation group, then a laboratory or nutrient field. '
                      'Grouping is visual only: nutrient fields retain their existing flat identifiers.'
                      if nutrient else 'Browse the documentation subsections. These describe the specification, '
                      'not fields in a hay record.' if section_id == 'metadata' else
                      'Choose a field from the outline. Expand a component to see its '
                      'members. Repeated lists describe one set of members per entry.'),
        'notice': ('Read each definition for units, reporting basis, and sample context. '
                   'Typical ranges in prose are not hard rejection limits. This guide does not '
                   'convert units, calculate values, or judge feeding suitability.' if nutrient else None),
    }
    # This is JSON inside a script element: prevent source text ending the element.
    payload = json.dumps(data, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    template = (Path(__file__).parent / 'templates' / 'field-guide.html').read_text()
    title = section.get('title', section_id)
    intro = ('Explore laboratory provenance, sample basis, and nutrient measurements. '
             'Browse a navigation group or search for an exact field identifier.' if nutrient else
             'Understand how a hay lot connects to its identifiers and contributing production fields. '
             'Explore the outline, then read a field in context.' if section_id == 'traceability' else
             'Explore the specification’s authorship, licensing, history, and publication context.'
             if section_id == 'metadata' else
             'Explore field definitions, their context, and any nested members. '
             'Choose a field or search for its exact identifier.')
    return (template.replace('__SECTION_TITLE__', escape(title))
            .replace('__SECTION_INTRO__', escape(intro))
            .replace('__REFERENCE__', f'../fields/{section_id}/')
            .replace('__GUIDE_DATA__', payload))


def section_cards(spec, prefix="", css_class="card"):
    """Render shared section links directly from the canonical section list."""
    cards = []
    for section in spec['sections']:
        identity = section['id']
        cards.append('<a class="' + escape(css_class, quote=True) + '" href="' +
                     escape(prefix + identity + '.html', quote=True) + '">'
                     '<h2>' + escape(section.get('title', identity)) + '</h2><p>' +
                     escape(re.split(r'(?<=[.!?])\s+', section.get('description', '').strip(), maxsplit=1)[0]) + '</p></a>')
    return '\n'.join(cards)


def guide_index(spec):
    """Link every canonical section, without presenting sections as record envelopes."""
    template = (Path(__file__).parent / 'templates' / 'field-guide-index.html').read_text()
    state = ('Published snapshot' if spec.get('publication_status') == 'published'
             else 'Unreleased working reference')
    return (template.replace('__GUIDE_CARDS__', section_cards(spec))
            .replace('__SOURCE_CONTEXT__', escape('Source ' + spec['version'] + ' · ' + state)))


def home_page(spec):
    """A guide-first entrance; source downloads remain exact transcriptions."""
    cards = section_cards(spec, prefix="guides/", css_class="lode-guide-card")
    state = ('Published snapshot' if spec.get('publication_status') == 'published'
             else 'Current working specification · includes unreleased changes')
    return ("---\nhide:\n  - navigation\n  - toc\n---\n\n"
            '<div class="lode-home" data-technical-overview="guidance/specification/">\n'
            '<p class="eyebrow">LODE / HAY DESCRIPTION SPECIFICATION</p>\n'
            '<h1>Explore the specification</h1>\n'
            '<p>Choose a field guide to understand each field and its relationships. '
            'Open a field’s complete source definition for every detail, or read about the specification.</p>\n'
            '<p class="publication">' + escape(state) + ' · source version ' + escape(spec['version']) +
            ' · status: ' + escape(spec['status']) + '.</p>\n'
            '<div class="downloads"><a href="source/hay-spec.yaml" download="hay-spec.yaml">Download YAML</a>'
            '<a href="source/hay-spec.json" download="hay-spec.json">Download JSON</a>'
            '<a href="guidance/specification/">About the specification</a><a href="guidance/index.html">Guidance and history</a></div>\n'
            '<p class="publication">Downloads reflect the current source. JSON is a transcription, '
            'not JSON Schema or a hay-record validator. For immutable snapshots, visit '
            '<a href="https://github.com/lode-global/hay-spec/releases">published releases</a>.</p>\n'
            '<div class="lode-guide-grid">' + cards + '</div>\n'
            '<p>Sections organize the documentation; they do not create new record envelopes. '
            'Existing identifiers, values, and nesting are preserved. '
            '<a href="history/reconciliation/">Read the reconciled history and original archive</a>.</p>\n'
            '</div>\n')
