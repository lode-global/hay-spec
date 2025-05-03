# Hay description specification

## Introduction

This document introduces a structured data model for describing hay in a standardized, machine-readable format. It aims to improve clarity, consistency, and efficiency in how hay is characterized, traded, and analyzed—whether in domestic or international markets.

**Hay is a foundational agricultural commodity**, essential to the nutrition of dairy and beef cattle, horses, goats, camels, sheep, and other animals. In the United States, hay ranks among the leading cash crops by annual sales value, alongside corn, wheat, and soybeans. Yet unlike those crops, hay is traded entirely on an over-the-counter basis—through peer-to-peer negotiation, dealers, or brokers—without common product definitions or standardized digital tools.

The hay market does not inherently require centralized exchanges to function well. But it does suffer from **two critical deficiencies**:

1. Buyers and sellers struggle to find one another efficiently.
2. There is limited electronic facilitation of trading, particularly in matching, documentation, and decision support.

These limitations stem in part from the lack of shared standards. Without consistent product descriptions or data conventions, hay listings and negotiations rely on informal descriptions, resulting in **persistent mismatches in perceptions of quality**, weak price signals, and high friction in trade. This hinders regional and global commerce, limits market transparency, and slows investment in modern tools for production, logistics, testing, and quality control.

Efforts to standardize hay go back more than a century. **As recently as the late 19th century**, centralized hay markets operated in cities such as Boston, Chicago, and San Francisco. Since then, producer groups, academic institutions, extension agencies, and the U.S. Department of Agriculture have all proposed grading systems. But none has achieved enduring, widespread adoption.

Several developments now offer new opportunities for progress:

- **Hay exports are growing**, especially alfalfa, which now trades across borders under increasingly formalized standards.
- **Testing technologies have matured**, including laboratory-based wet chemistry and NIR spectroscopy.
- **Digital tools and platforms are emerging**, enabling traceability from field to bale.
- **Online infrastructure allows global coordination**, opening the door for community-led standards and interoperability.

This document proposes a formal product definition for hay—a structured data model that captures economically salient characteristics in a consistent format. Such a definition supports better listings, search, comparison, and traceability. Over time, it may also surface patterns in market behavior that inform the development of accepted grading practices.

This specification is published by Lode, a platform for improving transparency and connectivity in agricultural commodities markets. To participate or provide feedback, contact us at [insert email address] or visit lode.global.

This is a working draft subject to field testing and stakeholder refinement.

Planned additions include:

- A reference dataset of **forage varieties**, with identifiers and metadata.
- A registry of **forage analysis laboratories** supporting the specified testing methods and protocols.

## Field Naming Conventions

All field names in this specification follow these conventions:

- All lowercase letters (`a–z`)
- Words separated by a single underscore (`_`)
- No spaces, hyphens, slashes, or special characters
- Scientific abbreviations normalized to lowercase (e.g., `ph`, `ppm`, `tdn`)
- Numerical qualifiers separated by underscores (e.g., `1x`, `3x`)
- Units of measure placed at the end, separated by underscores (e.g., `mcal_lb`, `percent_dm`)
- No trailing or double underscores

> **Example**: `digestible_energy_1x_mcal_lb`

## Traceability

This section captures whether the hay can be traced to a clearly defined production lot and whether formal identifiers exist that facilitate lot-level tracking, recall, or certification. Traceability is increasingly important in high-value or regulated markets, as it supports inventory segregation, quality assurance, documentation of origin, and post-sale issue resolution.

### `hay_single_lot_traceable`
- **Data type**: `boolean`  
- **Valid values**: A boolean value: `true` if the hay originates from a single, defined lot harvested under uniform agronomic and environmental conditions; `false` otherwise.

<details>
  <summary>More information about <code>hay_single_lot_traceable</code></summary>

  <p>Affirms whether the hay being described originates from a single, defined lot, harvested under uniform agronomic and environmental conditions. A lot is defined as "forage taken from the same farm, field, and cut under uniform conditions within a 48-hour time period," as described in <a href="https://fyi.extension.wisc.edu/forage/files/2017/04/FQ.pdf" target="_blank">Ball et al. (2001)</a> [PDF].</p>

  <p>This designation supports clarity in nutritional representation, quality assessment, and logistical consistency.</p>

</details>

### `lot_identifier_internal`
- **Data type**: `string`  
- **Valid values**: A free-text string up to 100 characters, representing an internal lot identifier defined by the producer for traceability and recordkeeping.

<details>
  <summary>More about <code>lot_identifier_internal</code></summary>

  <p>This field allows the seller to assign an internal identifier to the lot from which the hay originated. It may reflect farm, field, cutting, or date conventions relevant to the seller’s operation. Systems should enforce a character limit of 100 to ensure consistency and compatibility.</p>

  <p>Internal lot identifiers do not need to conform to any industry standard but should be unique within the seller’s system. They may be used for inventory management, customer reference, and traceability across quality or testing modules.</p>

</details>

### `lot_identifier_external`
- **Data type**: `component block`

#### `lot_identifier_external.value`
- **Data type**: `string`
- **Valid values**: A free-text value (max 100 characters) representing the external lot identifier.

<details>
  <summary>More about <code>lot_identifier_external.value</code></summary>

  <p>This field records the externally issued lot identifier assigned to the hay or forage lot by a regulatory, certifying, or export authority. Its meaning depends on the associated <code>lot_identifier_external.issuer</code> field, which specifies the organization or program responsible for issuing the identifier.</p>

  <p>External lot identifiers may appear on documents such as:</p>
  <ul>
    <li>Organic certificates (e.g., USDA NOP Lot #12345)</li>
    <li>Phytosanitary inspection reports</li>
    <li>Export documents or permits</li>
    <li>Weed-free forage program tags or declarations</li>
  </ul>

  <p>The value may include letters, numbers, or a combination thereof. Systems should enforce a maximum of 100 characters and preserve the identifier exactly as provided by the issuing body, including any dashes, slashes, or other formatting symbols.</p>

  <p>This field enhances traceability and may support validation workflows, especially in regulated or export-focused markets. When paired with a known <code>issuer</code>, it enables buyers and inspectors to independently confirm the status or eligibility of the hay lot.</p>

</details>

#### `lot_identifier_external.issuer`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ USDA | CFIA | State agriculture department | Export certification agency | Organic certifier | Weed-free program | Other ]`, representing the organization or program that issued the external lot identifier.

<details>
  <summary>More about <code>lot_identifier_external.issuer</code></summary>

  <p>This component field captures a formal lot identifier issued by an external authority, along with the issuing body or context in which the identifier was assigned.</p>

  <p>Common issuers include:
 
   <ul>
    <li><strong>USDA</strong> – e.g., for organic certification or phytosanitary control</li>
    <li><strong>CFIA</strong> – Canadian Food Inspection Agency</li>
    <li><strong>State agriculture department</strong> – e.g., for noxious weed-free programs or internal state grading systems</li>
    <li><strong>Export certification agency</strong> – e.g., for hay shipments requiring country-of-destination compliance</li>
    <li><strong>Organic certifier</strong> – third-party certifying bodies under the USDA NOP or equivalent foreign programs</li>
    <li><strong>Weed-free program</strong> – including NAISMA-affiliated programs</li>
    <li><strong>Other</strong> – catch-all for custom or less common issuers</li>
  </ul></p>

  <p>This structure allows systems and reviewers to assess the origin and regulatory weight of the identifier and may facilitate future API integrations or document uploads.</p>

</details>

### `lot_mapping_field_to_bale_supported`
- **Data type**: `boolean`  
- **Valid values**: A boolean value: `[ true | false ]`, indicating whether field-to-bale traceability is supported.

<details>
  <summary>More about <code>lot_mapping_field_to_bale_supported</code></summary>

  <p>This field indicates whether the seller maintains a system (digital or physical) for mapping specific bales or sub-lots to field-level characteristics, such as GPS coordinates, yield zones, or harvest time blocks.</p>

  <p>Such mapping enables greater traceability, enhances data resolution for quality control, and may support integration with field data platforms or precision agriculture systems. This capability is optional but increasingly valuable in transparent or regulated feed markets.</p>

</details>

---

**Summary Guidance**  
Traceability fields should be completed to the extent feasible. While not all buyers require formal lot tracking, inclusion of traceability data — especially internal and external identifiers — can streamline certification workflows, support inventory segregation, and build buyer confidence. Systems should validate consistency between `hay_single_lot_traceable` and identifier fields and may allow optional linking to field- or bale-level metadata for advanced users.
  
## Stand composition and agronomic characteristics

This section describes the planted forage stand—the biological and agronomic foundation of the hay crop. It includes the intended composition of plant varieties, their representation in the harvested hay, and related agronomic details such as establishment method, density, and maturity at harvest.

These fields support transparency around crop planning, species selection, and cultural practices, helping buyers assess the identity, uniformity, and development stage of the forage. The section also captures information relevant to quality, palatability, and intended use, and it helps agricultural professionals interpret how the hay’s characteristics relate to field management decisions.

### `stand_mixture_intended`
- **Data type**: `boolean`
- **Valid values**: A boolean value: `[ true | false ]`, indicating whether the stand was intentionally planted as a species mixture.

<details>
  <summary>More about <code>stand_mixture_intended</code></summary>

  <p>This field expresses whether the grower intended to plant a mixed stand (polyculture) or a pure stand (monoculture) of forage species. A value of <code>true</code> indicates the intention to grow a mix of species or varieties; a value of <code>false</code> indicates a monoculture was intended.</p>

  <p>This field captures grower intent and does not reflect the final outcome, which may differ due to environmental or agronomic factors. For example, a grower may plant an alfalfa/timothy mix, but only the timothy survives to harvest. This field would still be <code>true</code>.</p>

  <p>This field pairs with <code>forage_species_type</code>, which records the actual species composition of the forage at harvest, and with the <code>hay_variety_instances</code> group, which captures the grower’s target and achieved representation of each variety.</p>

</details>

### `forage_species_type`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ grass | legume | grass/legume mix | other ]`, representing the observed species composition of the forage at harvest.

<details>
  <summary>More about <code>forage_species_type</code></summary>

  <p>This field describes the biological classification of the forage species present in the hay at harvest. It reflects the **actual** or **observed** composition, rather than the grower's original intention.</p>

  <ul>
    <li><code>grass</code>: The hay consists primarily of grasses, such as bermudagrass or orchardgrass.</li>
    <li><code>legume</code>: The hay consists primarily of legumes, such as alfalfa or clover.</li>
    <li><code>grass/legume mix</code>: Both grasses and legumes are present in significant proportion.</li>
    <li><code>other</code>: The forage does not fit into the above categories (e.g., brassicas, forbs, or specialty hays).</li>
  </ul>

  <p>This field supports downstream applications such as nutritional analysis, ration formulation, and marketing. It is best determined based on post-harvest visual inspection or lab analysis, and complements <code>stand_mixture_intended</code>.</p>

</details>

### `forage_variety_count`
- **Data type**: `int`
- **Valid values**: A positive integer representing the number of distinct forage varieties present in the harvested hay crop.

<details>
  <summary>More about <code>forage_variety_count</code></summary>

  <p>This field reports how many distinct forage varieties were identified in the actual harvested crop. It supports both marketing claims (e.g., "two-variety blend") and technical purposes, such as determining how many instances of a <code>forage_variety_component</code> block will be included in a structured message.</p>

  <p>This field reflects actual harvest outcome, not grower intent. By contrast, <code>stand_mixture_intended</code> expresses whether the grower intended a mixed or pure sward. These two fields together help distinguish between intent and result.</p>

  <p>In a pure crop, this field should take a value of <code>1</code>. In a mixed crop, this field should take a value of <code>2</code> or more. If no species or varieties can be positively identified, the value should be <code>0</code>, and the <code>forage_species_type</code> should be set to <code>unknown</code>.</p>

  <p>System validations may check for consistency across <code>stand_mixture_intended</code>, <code>forage_variety_count</code>, and any listed <code>forage_variety_component</code> entries.</p>

</details>

### `forage_variety_components`
- **Data type**: `list` (repeating block)
- **Valid values**: One or more instances of the following component block, repeated once per forage variety in the sward.

<details>
  <summary>More about <code>forage_variety_components</code></summary>

  <p>This block describes each intentionally planted forage variety in the hay sward. Pure (monoculture) hay includes one instance; mixed (polyculture) hay includes two or more.</p>

  <p>Each entry should reflect the grower’s intention, variety name, and estimated contribution to the harvested crop. This supports both agronomic analysis and marketplace transparency.</p>

  <p>Use this block in combination with <code>forage_variety_count</code> and <code>stand_mixture_intended</code> to document crop composition and stand complexity.</p>

</details>

#### `forage_variety`
- **Data type**: `enum`
- **Valid values**: A specific forage species, subspecies, or named variety — drawn from a reference list maintained by Lode or another recognized organization.

<details>
  <summary>More about <code>forage_variety</code></summary>

  <p>Enter the full name of the forage variety, such as <code>Tifton 85 bermudagrass</code> or <code>Vernal alfalfa</code>. When possible, include binomial nomenclature, common name, and GMO status if known or relevant.</p>

  <p>Standardizing variety names supports better market searchability, agronomic traceability, and nutrient expectation setting.</p>

</details>

---

#### `variety_representation_target`
- **Data type**: `int`
- **Valid values**: A non-negative whole number representing the grower’s intended ratio for this variety at the time of planting.

<details>
  <summary>More about <code>variety_representation_target</code></summary>

  <p>This field captures the <em>intended</em> proportion of a given forage variety in the seed mix or planting strategy. Use whole-number ratios to reflect seeding intention. For example, if the mix was designed to be 3 parts orchardgrass and 1 part alfalfa, enter <code>3</code> for orchardgrass and <code>1</code> for alfalfa.</p>

  <p>This is not a percentage and does not need to sum to 100 — it simply expresses the intended relative ratio among varieties listed. The system or UI can calculate proportional percentages based on the total of all entries.</p>

  <p>This data helps buyers and agronomists understand the seeding strategy, even when outcomes differ due to growing conditions, weather, or stand establishment success.</p>

</details>

---

#### `variety_representation_result`
- **Data type**: `int`
- **Valid values**: An estimated whole number percentage (0–100) representing this variety’s actual visual or analytical presence in the harvested hay.

<details>
  <summary>More about <code>variety_representation_result</code></summary>

  <p>This field captures the <em>observed</em> contribution of this variety in the finished hay. Enter a percentage value, based on best available knowledge — such as visual inspection, lab composition, or grower experience.</p>

  <p>This value is distinct from the <code>variety_representation_target</code>, which describes the planting ratio. The <code>result</code> reflects reality after accounting for environmental factors like stand failure, overgrowth of one species, weed intrusion, or management effects.</p>

  <p>Use whole numbers (e.g., <code>65</code> for 65%) and aim for total values across all components to sum to approximately 100%. Minor discrepancies are acceptable when reporting is based on visual estimates.</p>

</details>

**End of repeating section. Resume standard field definitions below.**

### `stand_maturity_at_harvest`
- **Data type**: `enum`
- **Valid values**:**Valid values**: An enumerated value representing the predominant maturity stage of the forage at harvest. Use the grass scale (`[ vegetative | early head | mid head | full head | post-head ]`) for grass hays, and the legume scale (`[ vegetative | bud | early bloom | full bloom | post-bloom ]`) for alfalfa and similar legumes.

<details>
  <summary>More about <code>stand_maturity_at_harvest</code></summary>

  <p>This field records the predominant maturity stage of the forage stand at the time of harvest. Maturity at harvest strongly influences forage quality, including digestibility, fiber content, and crude protein.</p>

  <p>Use the appropriate scale depending on whether the crop is primarily a grass or a legume such as alfalfa:</p>

  <ul>
    <li><strong>Grass scale</strong>: Used for species like bermudagrass, orchardgrass, or timothy.</li>
    <li><strong>Alfalfa scale</strong>: Used for alfalfa or clover-dominant stands.</li>
  </ul>

  <p>Selection of the correct maturity stage allows buyers and nutritionists to better anticipate hay characteristics and plan for optimal livestock feeding strategies.</p>

</details>

### `stand_establishment_method`
- **Data type**: `enum`
- **Valid values**: An enumerated value representing the method used to establish the forage stand. Typical options include `[ drilled | broadcast | no-till | sod-seeded | unknown ]`.

<details>
  <summary>More about <code>stand_establishment_method</code></summary>

  <p>This field indicates the method used to establish the forage stand. Establishment method can affect plant density, weed suppression, and long-term stand performance.</p>

</details>

### `stand_establishment_date`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing when the forage stand was planted or sown. Use double zeroes in the day or month fields if the exact date is unknown.

<details>
  <summary>More about <code>stand_establishment_date</code></summary>

  <p>This field records the date on which the stand was planted or sown. If the exact day is unknown, a double-zero convention may be used in the day and/or month fields (e.g., <code>20240400</code> for April 2024).</p>

</details>

### `stand_density`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ sparse | moderate | dense | unknown ]`, representing the observed density of the forage stand at harvest.

<details>
  <summary>More about <code>stand_density</code></summary>

  <p>This field qualitatively assesses the density of the forage stand at time of harvest. Higher density can indicate better competition with weeds and improved yield.</p>

</details>

### `source_stand_age`
- **Data type**: `int`
- **Valid values**: A non-negative integer representing the age of the forage stand in years at the time of harvest.

<details>
  <summary>More about <code>source_stand_age</code></summary>

  <p>This field records the number of years the current forage stand has been in place at the time of harvest. It reflects how long the same root system and plant population have been producing harvestable hay from the same field without replanting or reseeding.</p>

  <p>Newly established stands may offer better vigor and fewer weeds, while older stands may show declining productivity, species composition shifts, or increased weed pressure.</p>

  <p>Enter <code>0</code> if this is the first year of the stand's establishment. This field is especially important for perennial forages such as alfalfa, bermudagrass, or orchardgrass.</p>

</details>

## Field location and growing environment

This section describes the field location and environmental characteristics where the hay was produced. Geographic factors play a significant role in hay quality, influencing aspects such as nutrient content, texture, and palatability. Elevation, climate classification, and irrigation infrastructure all shape growing conditions and harvesting outcomes.

These fields support traceability, enable regional comparisons, and help buyers assess how site-specific factors may affect hay performance for their intended use.

### `hay_origin_country_code`
- **Data type**: `string`  
- **Valid values**: A two-character string from the ISO 3166-1 alpha-2 code list, representing the applicable, two-letter code for country of origin.

<details>
  <summary>More about <code>hay_origin_country_code</code></summary>

  <p>This field specifies the country in which the hay was produced, using the standardized ISO 3166-1 alpha-2 code set. Examples include <code>US</code> for the United States, <code>CA</code> for Canada, and <code>MX</code> for Mexico.</p>

  <p>Using this internationally recognized format allows for consistent and automated identification of national origin across systems and jurisdictions. This field supports traceability, compliance with import/export requirements, and transparency for buyers concerned with geographic sourcing.</p>

  <p>System interfaces may implement dropdown menus or auto-complete fields linked to an official ISO 3166-1 code list to minimize user input errors.</p>

  <p>A full list of ISO 3166-1 alpha-2 country codes is available here:  
  <a href="https://www.iso.org/iso-3166-country-codes.html" target="_blank">ISO 3166-1 country codes [ISO.org]</a></p>

</details>

### `hay_origin_subdivision_code`
- **Data type**: `string`  
- **Valid values**: A standardized code from the ISO 3166-2 list, representing the principal administrative subdivision (e.g., state, province, or region) of the country in which the hay was produced.

<details>
  <summary>More about <code>hay_origin_subdivision_code</code></summary>

  <p>This field specifies the first-level administrative region associated with the hay’s origin, using the ISO 3166-2 code format. The full code typically includes the country code followed by a hyphen and a subdivision identifier (e.g., <code>US-TX</code> for Texas, United States).</p>

  <p>Consistent use of ISO 3166-2 subdivision codes allows for clear geographic traceability and regional classification across jurisdictions. This field can be used for compliance tracking, climate zone mapping, and regional market analysis.</p>

  <p>System interfaces may present the user with filtered subdivision options once a country code is selected, reducing data entry errors and enhancing usability.</p>

  <p>A reference list of ISO 3166-2 subdivision codes is available here:  
  <a href="https://www.iso.org/iso-3166-country-codes.html" target="_blank">ISO 3166-2 subdivision codes [ISO.org]</a></p>

</details>

### `hay_origin_county`
- **Data type**: `string`
- **Valid values**: A free-text string up to 100 characters representing the name of the county or equivalent third-level administrative unit where the hay was produced.

<details>
  <summary>More about <code>hay_origin_county</code></summary>

  <p>This field records the county, parish, district, or other subnational jurisdiction in which the hay was grown. It provides more granular geographic detail than country or subdivision codes and may be important for local traceability, extension service classification, or compliance with region-specific programs.</p>

  <p>Because standardized naming varies across countries and regions, this field is implemented as a free-text entry. However, implementing systems may optionally use a lookup table or restrict input to known county names within the selected subdivision and country.</p>

  <p>This field complements <code>hay_origin_country_code</code> and <code>hay_origin_subdivision_code</code> in forming a complete geographic trace of the product’s source. To maintain compatibility with downstream systems and prevent excessively long entries, input should not exceed 100 characters.</p>

</details>

### `hay_origin_postal_code`
- **Data type**: `string`
- **Valid values**: A postal or ZIP code string appropriate to the country and region where the hay was produced, with a maximum length of 20 characters.

<details>
  <summary>More about <code>hay_origin_postal_code</code></summary>

  <p>This field captures the postal code (or ZIP code) for the location where the hay was grown. It offers a standardized method for identifying origin at a highly localized level and may support integration with mapping, logistics, or regional compliance systems.</p>

  <p>Postal codes vary in format by country (e.g., <code>90210</code> in the U.S., <code>K1A 0B1</code> in Canada, <code>75008</code> in France). This field accepts any format valid in the associated <code>hay_origin_country_code</code>, up to 20 characters in total length.</p>

  <p>Implementing systems may optionally validate against country-specific postal code patterns or offer auto-complete features based on the selected country and subdivision.</p>

  <p>This field complements <code>hay_origin_country_code</code>, <code>hay_origin_subdivision_code</code>, and <code>hay_origin_county</code> for full geographic traceability.</p>

</details>

### `source_field_elevation`
- **Data type**: `int`
- **Valid values**: A positive or negative integer representing elevation in meters or feet above or below sea level, depending on the units specified in `source_field_elevation_units`.

<details>
  <summary>More about <code>source_field_elevation</code></summary>

  <p>This field captures the elevation of the field in which the hay was grown. Elevation can influence temperature, growing degree days, and forage composition.</p>

  <p>Importantly, all else being equal, higher elevations tend to correlate with lower lignin levels—resulting in softer, more palatable hay. This makes elevation an indirect but meaningful indicator of potential forage quality.</p>

  <p>Enter a numeric value corresponding to the elevation of the field’s center point, rounded to the nearest whole number. If elevation is below sea level, use a negative integer.</p>

  <p>This field must be interpreted in conjunction with the associated <code>source_field_elevation_units</code> field, which clarifies whether the value is in <code>meters</code> or <code>feet</code>.</p>

  <p>Elevation data may be obtained from GPS tools, topographic maps, or online elevation services based on coordinates or postal code.</p>

</details>

### `source_field_elevation_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ meters | feet ], representing the unit of measurement used for field elevation.

<details>
  <summary>More about <code>source_field_elevation_units</code></summary>

  <p>This field specifies the unit of measurement used in the <code>source_field_elevation</code> field. Accurate unit identification is essential for interpreting elevation values correctly and ensuring consistent data across systems.</p>

  <p>
    <strong>meters</strong>: Elevation is expressed in meters above or below sea level.<br>
    <strong>feet</strong>: Elevation is expressed in feet above or below sea level.
  </p>

  <p>When implementing this standard in software systems, consider validating elevation values for plausibility within the chosen unit. For example, elevations exceeding 9,000 meters or 30,000 feet may require review.</p>

  <p>This field enables flexibility for global users who may record elevation data in different systems of measurement, while ensuring clarity for comparison and analysis.</p>

</details>

### `source_field_climate_class`
- **Data type**: `string`
- **Valid values**: A valid Köppen-Geiger climate classification code (e.g., `Cfa`, `BSk`, `Dfb`) representing the general climate type of the source field.

<details>
  <summary>More about <code>source_field_climate_class</code></summary>

  <p>This field records the generalized climate classification for the field where the hay was grown, using the widely recognized <a href="https://en.wikipedia.org/wiki/K%C3%B6ppen_climate_classification" target="_blank">Köppen-Geiger climate classification</a> system. Examples include:</p>

  <ul>
    <li><code>Cfa</code> – Humid subtropical (e.g., Southeastern United States)</li>
    <li><code>BSk</code> – Cold semi-arid (e.g., High Plains)</li>
    <li><code>Dfb</code> – Humid continental, warm summer (e.g., Northern Midwest)</li>
  </ul>

  <p>Including this classification provides context about growing conditions such as temperature range, precipitation patterns, and seasonal variation. These factors can influence forage species selection, nutrient density, and cutting intervals.</p>

  <p>System implementations may allow the user to select from a predefined list or map climate zones automatically based on location data. Values must conform to the standard Köppen-Geiger codes, typically in 2–3 letter formats.</p>

</details>

### `source_field_area`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the area of the source field, measured in units specified by the `source_field_area_units` field.

<details>
  <summary>More about <code>source_field_area</code></summary>

  <p>This field captures the size of the field or parcel from which the hay was harvested. Field area is relevant for assessing yield per acre/hectare, validating production claims, and understanding the scale of the operation.</p>

  <p>Values should be entered as positive decimal numbers. Round to the nearest <code>0.1</code> unit unless greater precision is available or required. For example, a field that is approximately twenty-two and a half acres would be recorded as <code>22.5</code>.</p>

  <p>The appropriate unit of measure must be declared in the associated <code>source_field_area_units</code> field. If multiple fields contributed to the lot, enter the combined area. System interfaces may offer auto-calculation based on linked parcel data.</p>

</details>

### `source_field_area_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ acres | hectares ]`, representing the unit of measurement used to express the field area.

<details>
  <summary>More about <code>source_field_area_units</code></summary>

  <p>This field specifies the unit of measurement used in the <code>source_field_area</code> field. Standardizing units ensures clarity in reporting and comparability across listings and geographies.</p>

  <ul>
    <li><code>acres</code>: Commonly used in the United States and a few other countries. One acre equals 43,560 square feet or approximately 0.405 hectares.</li>
    <li><code>hectares</code>: The standard metric unit of land area, equal to 10,000 square meters or approximately 2.471 acres.</li>
  </ul>

  <p>Users should select the unit most appropriate for their region or reporting needs. System implementations may convert between units internally but should always preserve the original unit used for input and display.</p>

</details>

### `irrigation_status`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ rainfed only | irrigation available | irrigation required ]`, representing the general water source context for hay production.

<details>
  <summary>More about <code>irrigation_status</code></summary>

  <p>This field describes the general irrigation context in which the hay was grown:</p>

  <ul>
    <li><code>rainfed only</code>: Crop is typically grown without any irrigation; relies solely on rainfall.</li>
    <li><code>irrigation available</code>: Irrigation systems are available to supplement rainfall, but are not always necessary.</li>
    <li><code>irrigation required</code>: Reliable irrigation is essential for growing this hay crop in the region or operation.</li>
  </ul>

  <p>This field offers buyers insight into crop reliability, regional water dependency, and resilience under dry conditions.</p>

</details>

### `irrigation_method_available`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ none | flood | sprinkler | pivot | drip ]`, representing the primary irrigation method available to the producer.

<details>
  <summary>More about <code>irrigation_method_available</code></summary>

  <p>This field indicates the primary irrigation method available to the producer:</p>

  <ul>
    <li><code>none</code>: No irrigation equipment or systems are available.</li>
    <li><code>flood</code>: Water is distributed by gravity over the field.</li>
    <li><code>sprinkler</code>: Water is applied using static or movable sprinkler systems.</li>
    <li><code>pivot</code>: A rotating center-pivot system is used to apply water in a circular pattern.</li>
    <li><code>drip</code>: Water is delivered directly to the root zone through emitters or tubing.</li>
  </ul>

  <p>This field complements <code>irrigation_status</code> by describing technical capacity rather than agronomic necessity.</p>

</details>

### Validation Note: Harmonization of `irrigation_status` and `irrigation_method_available`

<details>
  <summary>Cross-field consistency guidance</summary>

  <p>The fields <code>irrigation_status</code> and <code>irrigation_method_available</code> describe related but distinct aspects of water management in hay production:</p>

  <ul>
    <li><strong><code>irrigation_status</code></strong> expresses the agronomic need or reliance on irrigation.</li>
    <li><strong><code>irrigation_method_available</code></strong> identifies the specific system or method available to the grower, if any.</li>
  </ul>

  <p>To ensure internal consistency, systems implementing this schema may apply the following validation logic:</p>

  <ul>
    <li>If <code>irrigation_status</code> = <code>rainfed only</code>, then <code>irrigation_method_available</code> should be <code>none</code>.</li>
    <li>If <code>irrigation_status</code> = <code>irrigation required</code>, then <code>irrigation_method_available</code> must not be <code>none</code>.</li>
    <li>If <code>irrigation_status</code> = <code>irrigation available</code>, then <code>irrigation_method_available</code> must not be <code>none</code>.</li>
  </ul>

  <p>This validation supports interpretability, consistency across records, and trust in the reported production context.</p>

</details>

### `irrigation_method_used`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ none | flood | sprinkler | pivot | drip | unknown ]`, representing the primary irrigation method actually used during the most recent production cycle.

<details>
  <summary>More about <code>irrigation_method_used</code></summary>

  <p>This field records the primary irrigation method actually used by the grower during the most recent production cycle of the hay crop.</p>

  <ul>
    <li><code>none</code>: No irrigation was applied; the crop was fully rainfed.</li>
    <li><code>flood</code>: Irrigation water was distributed by gravity flow across the soil surface.</li>
    <li><code>sprinkler</code>: Irrigation was applied using stationary or movable sprinklers.</li>
    <li><code>pivot</code>: A center-pivot system was used to irrigate the crop.</li>
    <li><code>drip</code>: Water was delivered directly to the root zone using drip lines or emitters.</li>
    <li><code>unknown</code>: The grower or seller does not know or did not report the irrigation method used.</li>
  </ul>

  <p>This field complements <code>irrigation_method_available</code> by indicating which method was actually deployed, if any. It helps assess water inputs, agronomic practices, and environmental conditions influencing the crop's growth and final quality.</p>

</details>

## Soil and field management

This section captures how the grower prepares and maintains the soil to support a healthy forage stand. It includes information about fertilizer applications, soil amendments, and general nutrient management. These practices influence crop yield, plant vigor, and nutritional quality of the harvested hay. They also help downstream users assess environmental practices, sustainability, and alignment with production goals (e.g., high-protein dairy forage vs. lower-input grazing hay).

Where applicable, fields differentiate between nutrient application to legume vs. grass crops—acknowledging, for example, that nitrogen is often unnecessary for legumes due to biological nitrogen fixation.

### `soil_test_date`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing when the most recent soil test was conducted, or `00000000` if no test was performed. Use double zeroes in the day or month fields if the exact date is not known.

<details>
  <summary>More about <code>soil_test_date</code></summary>

  <p>This field records the date of the most recent soil test used to guide nutrient and pH management decisions for the current hay crop. Soil testing helps optimize fertilizer and lime application, supports environmental stewardship, and informs yield and quality expectations.</p>

  <p>Enter the date in <code>YYYYMMDD</code> format. Use <code>00000000</code> if no test was conducted. If the exact day or month is unknown, you may use double-zero conventions: <code>YYYYMM00</code> for known month but unknown day, and <code>YYYY0000</code> for known year but unknown month and day.</p>

  <p>This field enhances transparency and may support future traceability or certification requirements.</p>

</details>

### `soil_test_ph`
- **Data type**: `float`
- **Valid values**: A float between `4.5` and `8.5`, representing the soil’s pH value as determined by the most recent soil test.

<details>
  <summary>More about <code>soil_test_ph</code></summary>

  <p>This field records the pH of the soil based on the most recent test. Soil pH affects nutrient availability, microbial activity, and crop performance. Most forage crops grow best in soils with a pH between <code>6.0</code> and <code>7.5</code>, though legumes like alfalfa perform best when pH is above <code>6.5</code>.</p>

  <p>If this field is used, its value should reflect a recent, lab-confirmed test. Systems may prompt for this field only if <code>soil_tested_recently = true</code>.</p>

  <p>Buyers and agronomists may use this value to evaluate crop suitability, field management, and potential nutrient deficiencies or toxicities.</p>

</details>

### `lime_applied`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether lime or a pH-adjusting amendment was applied to the field.

<details>
  <summary>More about <code>lime_applied</code></summary>

  <p>This field indicates whether agricultural lime or another pH-adjusting amendment was applied to the field prior to or during the hay crop cycle. Liming helps correct soil acidity and is particularly important for legumes like alfalfa, which require near-neutral pH for optimal growth.</p>

  <p>A value of <code>true</code> means lime was applied; <code>false</code> means it was not; <code>unknown</code> indicates the seller is unsure or has not tested the soil.</p>

  <p>Disclosing lime application supports transparency in soil fertility management and helps buyers understand underlying factors that may affect nutrient uptake and crop quality.</p>

</details>

### `lime_application_date`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing the most recent application of lime to the field.

<details>
  <summary>More about <code>lime_application_date</code></summary>

  <p>This field records the date on which lime was last applied to the field. Lime affects soil pH gradually, so knowing the timing helps interpret its likely influence on the current crop's root environment and nutrient uptake.</p>

  <p>If lime was applied multiple times, report the most recent date. If the exact date is unknown, use `YYYYMM00` or `YYYY0000` as appropriate, following the convention established for harvest and sample dates.</p>

  <p>Systems may prompt for this field only if <code>lime_applied = true</code>. This information supports traceability, fertility planning, and nutrient interaction modeling.</p>

</details>

### Fertilizer application dates

#### `date_fertilized_nitrogen`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing the last date of nitrogen fertilization for this hay.  
  Use `00000000` if no nitrogen fertilizer was applied.  
  Use `YYYYMM00` if the day is unknown.  
  Use `YYYY0000` if both month and day are unknown.

<details>
  <summary>More about <code>date_fertilized_nitrogen</code></summary>

  <p>This field captures the most recent application date of nitrogen fertilizer for the hay in question. Nitrogen fertilization is a key factor influencing crude protein levels, growth rate, and overall forage yield.</p>

  <p>Enter the date in <code>YYYYMMDD</code> format. If no nitrogen fertilizer was applied, enter <code>00000000</code>. If only the year is known, use <code>YYYY0000</code>. If the year and month are known but not the day, use <code>YYYYMM00</code>.</p>

  <p>Timely disclosure of nitrogen use helps buyers assess nitrate risk and understand expected nutrient content.</p>

</details>

#### `date_fertilized_potassium`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing the last date of potassium fertilization for this hay.  
  Use `00000000` if no potassium fertilizer was applied.  
  Use `YYYYMM00` if the day is unknown.  
  Use `YYYY0000` if both month and day are unknown.

<details>
  <summary>More about <code>date_fertilized_potassium</code></summary>

  <p>This field indicates the most recent application date of potassium fertilizer. Potassium supports plant water regulation, stress tolerance, and disease resistance — all of which influence forage quality and yield.</p>

  <p>Enter the date in <code>YYYYMMDD</code> format. If potassium fertilizer was not applied, enter <code>00000000</code>. If only the year is known, use <code>YYYY0000</code>. If the year and month are known but not the day, use <code>YYYYMM00</code>.</p>

  <p>Disclosing potassium use assists in evaluating stand health and potential forage longevity.</p>

</details>

#### `date_fertilized_phosphorus`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing the last date of phosphorus fertilization for this hay.  
  Use `00000000` if no phosphorus fertilizer was applied.  
  Use `YYYYMM00` if the day is unknown.  
  Use `YYYY0000` if both month and day are unknown.

<details>
  <summary>More about <code>date_fertilized_phosphorus</code></summary>

  <p>This field documents the most recent phosphorus application date. Phosphorus promotes root development, stand establishment, and early plant growth, making it critical for long-term forage productivity.</p>

  <p>Use the <code>YYYYMMDD</code> format for date entry. If phosphorus fertilizer was not used, enter <code>00000000</code>. If only the year is known, use <code>YYYY0000</code>. If the year and month are known but not the day, use <code>YYYYMM00</code>.</p>

  <p>Understanding phosphorus usage can help in evaluating early season vigor and assessing nutrient management strategies.</p>

</details>

### `amount_fertilized_nitrogen`
- **Data type**: `int`
- **Valid values**: An integer representing the magnitude, rounded to the nearest whole unit, of the last nitrogen application for this hay, or `0` if not nitrogen-fertilized.

Use the field <code>amount_fertilized_units</code> to specify the unit of measure for this magnitude.

<details>
  <summary>More about <code>amount_fertilized_nitrogen</code></summary>

  <p>This field captures the quantity of nitrogen applied during the most recent fertilization event. Nitrogen is a key nutrient influencing plant growth, crude protein levels, and overall yield.</p>

  <p>Use whole numbers only. If no nitrogen was applied, enter <code>0</code>.</p>

  <p>The unit of measure for this field is defined separately in the <code>amount_fertilized_units</code> field and must be interpreted in conjunction with that setting.</p>

</details>

### `amount_fertilized_potassium`
- **Data type**: `int`
- **Valid values**: An integer representing the magnitude, rounded to the nearest whole unit, of the last potassium application for this hay, or `0` if not potassium-fertilized.

Use the field <code>amount_fertilized_units</code> to specify the unit of measure for this magnitude.

<details>
  <summary>More about <code>amount_fertilized_potassium</code></summary>

  <p>This field specifies the quantity of potassium applied during the most recent fertilization event. Potassium enhances plant tolerance to drought and disease, supports stem strength, and improves forage quality.</p>

  <p>Use whole numbers only. If no potassium was applied, enter <code>0</code>.</p>

  <p>The unit of measure is provided separately in the <code>amount_fertilized_units</code> field and should be used in tandem with this value.</p>

</details>

### `amount_fertilized_phosphorus`
- **Data type**: `int`
- **Valid values**: An integer representing the magnitude, rounded to the nearest whole unit, of the last phosphorus application for this hay, or `0` if not phosphorus-fertilized.

Use the field <code>amount_fertilized_units</code> to specify the unit of measure for this magnitude.

<details>
  <summary>More about <code>amount_fertilized_phosphorus</code></summary>

  <p>This field indicates the quantity of phosphorus applied during the most recent fertilization event. Phosphorus is vital for root development, energy transfer, and early-season growth in forage crops.</p>

  <p>If no phosphorus was applied, enter <code>0</code>. Values must be expressed as whole numbers.</p>

  <p>The corresponding unit of measure is defined in the <code>amount_fertilized_units</code> field and must be interpreted together with this value.</p>

</details>

### `amount_fertilized_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ kilograms per hectare | pounds per acre ]`, representing the unit of measure used for reported fertilizer quantities.

<details>
  <summary>More about <code>amount_fertilized_units</code></summary>

  <p>This field specifies the unit of measure for all values entered in the fertilizer quantity fields: <code>amount_fertilized_nitrogen</code>, <code>amount_fertilized_potassium</code>, and <code>amount_fertilized_phosphorus</code>.</p>

  <p>Consistency in unit selection is required for accurate comparison and analysis. Choose only one unit system per entry, based on local or regulatory preference. For example, most U.S. producers will use <code>pounds per acre</code>, while metric-based countries will use <code>kilograms per hectare</code>.</p>

</details>

### `organic_amendments_applied`
- **Data type**: `list` (repeating block)
- **Valid values**: One or more instances of the following component block:

#### `amendment_type`
- **Data type**: `enum`
- **Valid values**: `[ compost | manure | cover crop residue | biochar | other ]`

<details>
  <summary>More about <code>amendment_type</code></summary>

  <p>This field identifies the type of organic material applied to the soil. Use <code>other</code> if the amendment does not fit the listed categories, and consider providing an explanation in supplemental fields if needed.</p>

</details>

#### `amendment_amount`
- **Data type**: `int`
- **Valid values**: A whole number representing the magnitude of the application, rounded to the nearest unit.

<details>
  <summary>More about <code>amendment_amount</code></summary>

  <p>This field records the quantity of the amendment applied. Use whole numbers for simplicity. The unit is defined in the <code>amendment_amount_units</code> field.</p>

</details>

#### `amendment_amount_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ tons per acre | tons per hectare | cubic yards per acre ]`, representing the unit of measure used to report amendment application rates.

<details>
  <summary>More about <code>amendment_amount_units</code></summary>

  <p>This field defines the unit of measurement used for the amendment quantity. Choose the most appropriate based on how the amendment was applied or recorded.</p>

</details>

#### `amendment_application_date`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing when the amendment was applied. Use `00000000` if unknown; double-zero format is allowed for unknown day or month.

<details>
  <summary>More about <code>amendment_application_date</code></summary>

  <p>This field captures the date the amendment was applied. This timing can influence nutrient availability, microbial activity, and impact on the crop.</p>

</details>

## Intended use and market context

This section captures the grower's intended livestock audience, production philosophy (including certifications), and other contextual factors relevant to how the hay is positioned in the market. These fields help buyers assess suitability for their specific animals, comply with regulatory or programmatic requirements (e.g., organic or weed-free sourcing), and identify potential constraints (e.g., GMO import restrictions).

### `intended_forage_use`
- **Data type**: `enum`  
- **Valid values**: An enumerated value representing the primary intended animal class or application for which the hay is marketed. Typical values include `[ Dairy | Beef | Horse | Goat | Sheep | Deer | Camel | Rabbit | Guinea pig | Tortoise | Zoo/Wildlife | Landscape | Other ]`.

<details>
  <summary>More about <code>intended_forage_use</code></summary>

  <p>This field identifies the primary intended animal class or application for which the hay or forage is marketed. It improves alignment between buyer needs and product suitability by signaling expected quality standards, palatability, and feed safety requirements.</p>

  <p>Valid values include:</p>
  
  <ul>
    <li><code>Dairy</code> – High-energy, high-protein, low-fiber forage suitable for lactating dairy cows</li>
    <li><code>Beef</code> – For growing, breeding, or finishing beef cattle with varied quality tolerance</li>
    <li><code>Horse</code> – Typically dust-free, low NSC forage with consistent texture and color</li>
    <li><code>Goat</code> – Moderate- to high-protein forage, tolerates stemmier material</li>
    <li><code>Sheep</code> – Requires attention to copper and energy levels; typically higher quality than beef forage</li>
    <li><code>Deer</code> – Highly digestible forage for farmed or captive cervids</li>
    <li><code>Camel</code> – Includes llamas, alpacas, and camels; suitable for coarser forage</li>
    <li><code>Rabbit</code> – High-fiber, low-calcium forage; typically small-stem grass hay</li>
    <li><code>Guinea pig</code> – Similar to rabbit requirements; may need stricter control on mold and texture</li>
    <li><code>Tortoise</code> – Drier, low-protein hays (e.g., timothy or orchardgrass)</li>
    <li><code>Zoo/Wildlife</code> – Regulated or specialized forage for zoological or rescue settings</li>
    <li><code>Landscape</code> – Erosion control, bedding, weed suppression, or decorative mulch</li>
    <li><code>Other</code> – Any unlisted use, including emerging or nontraditional forage markets</li>
  </ul>

  <p>Whether this field is implemented as a single- or multi-select option should be determined by the target platform. Many forages are marketed to multiple end-use types or across animal species.</p>

</details>

### `intended_use_case`
- **Data type**: `enum`
- **Valid values**: An enumerated value representing the functional purpose for which the hay was intended. Typical values include `[ maintenance | growth | lactation | work | general purpose | unknown ]`.

<details>
  <summary>More about <code>intended_use_case</code></summary>

  <p>This field captures the functional purpose for which the hay was intended — such as maintaining body condition, supporting growth, or producing milk.</p>

  <ul>
    <li><code>maintenance</code>: Intended for animals not in production (e.g., dry cows, idle horses).</li>
    <li><code>growth</code>: Designed to support young or growing animals.</li>
    <li><code>lactation</code>: Targeted for milk-producing animals with high energy/protein demand.</li>
    <li><code>work</code>: For animals performing physical labor (e.g., working horses).</li>
    <li><code>general purpose</code>: No specific function; applicable to various use cases.</li>
    <li><code>unknown</code>: Intention not known or disclosed.</li>
  </ul>

  <p>This metadata helps buyers evaluate whether the hay aligns with their nutritional goals and may inform expected quality ranges.</p>

</details>

### `gmo_presence_status`
- **Data type**: `enum`
- **Valid values**: An enumerated value representing the GMO status of the hay crop, including certification status if applicable. Valid options include `[ GMO | non-GMO certified | non-GMO (uncertified) | unknown ]`.

<details>
  <summary>More about <code>gmo_presence_status</code></summary>

  <p>This field describes whether the hay was produced from a genetically modified crop, and if applicable, whether non-GMO status is supported by formal certification.</p>

  <ul>
    <li><code>GMO</code>: Hay was produced from a genetically modified crop (e.g., Roundup Ready alfalfa).</li>
    <li><code>non-GMO certified</code>: Hay was produced from a non-GMO crop and has been certified by a recognized non-GMO verification program.</li>
    <li><code>non-GMO (uncertified)</code>: The producer affirms that the hay is non-GMO but has not obtained formal certification.</li>
    <li><code>unknown</code>: GMO status of the source crop is not known or not disclosed.</li>
  </ul>

  <p>Examples of recognized non-GMO certification or verification programs include:</p>

  <ul>
    <li><strong>Non-GMO Project Verified</strong></li>
    <li><strong>USDA Organic</strong> (Note: While not a GMO-specific program, USDA Organic prohibits GMO use)</li>
    <li><strong>Certified Naturally Grown</strong> (if accompanied by GMO-free attestation)</li>
    <li><strong>EU Organic Certification</strong> (Regulation (EU) 2018/848)</li>
  </ul>

  <p>This field is particularly important for export, specialty feed, and organic markets, where GMO crops may be restricted or excluded by regulation or buyer preference. For instance:</p>

  <ul>
    <li><strong>European Union:</strong> Requires labeling of feed products containing more than 0.9% GMO content. Products exceeding this threshold must be clearly labeled, impacting marketability of GMO hay in EU countries. <a href="https://maint.loc.gov/law/help/restrictions-on-gmos/index.php">Source</a></li>
    <li><strong>Mexico:</strong> Has implemented restrictions on GMO corn imports, particularly for human consumption, leading to trade disputes under the USMCA. While these measures primarily target corn, they reflect a broader regulatory stance that could affect other GMO products, including hay. <a href="https://www.wilsoncenter.org/article/gmo-corn-case-and-north-american-integration-sin-maiz-no-hay-pais-meets-king-corn">Source</a></li>
  </ul>

  <p>Accurate classification enhances transparency, supports marketing claims, and helps ensure regulatory compliance.</p>

</details>

### `production_certification_status`
- **Data type**: `enum` (multi-select allowed)
- **Valid values**: An enumerated list representing the production-related certifications applicable to the hay. Multiple selections allowed. Options include `[ certified organic | certified non-GMO | certified weed free | transitional organic | none | unknown ]`.

<details>
  <summary>More about <code>production_certification_status</code></summary>

  <p>This field captures the production-related certifications or designations that apply to the hay. These certifications provide assurance to buyers about how the hay was grown and handled and may influence eligibility for certain markets or programs.</p>

  <ul>
    <li><code>certified organic</code> – The hay is certified organic under a recognized program (e.g., USDA NOP, EU Organic).</li>
    <li><code>certified non-GMO</code> – The hay is certified to contain no genetically modified organisms, verified by a recognized non-GMO certification program.</li>
    <li><code>certified weed free</code> – The hay has been certified as noxious weed-free, often required for forage transported into public lands, parks, or certain export markets.</li>
    <li><code>transitional organic</code> – The hay is being grown under organic-compliant practices but is not yet fully certified; often used in multi-year transition periods.</li>
    <li><code>none</code> – The hay is not certified under any of the above categories.</li>
    <li><code>unknown</code> – The certification status is not known or not disclosed by the seller.</li>
  </ul>

  <p>This field supports multiple selections to reflect cases where hay qualifies under more than one certification (e.g., both <code>certified organic</code> and <code>certified weed free</code>).</p>

  <p>System implementations should allow users to select one or more values and validate input accordingly.</p>

</details>

### `distribution_channel`
- **Data type**: `enum`
- **Valid values**: An enumerated value representing the primary distribution scope of the hay. Options include `[ local | regional | national | export | unknown ]`.

<details>
  <summary>More about <code>distribution_channel</code></summary>

  <p>This field captures the primary distribution context or market scope for which the hay was prepared. It can help infer quality standards, packaging format, and logistics expectations.</p>

  <ul>
    <li><code>local</code>: Intended for use within the immediate community or county.</li>
    <li><code>regional</code>: Distributed across a multi-county or state/province area.</li>
    <li><code>national</code>: Distributed across the entire country.</li>
    <li><code>export</code>: Intended for international sale or shipping.</li>
    <li><code>unknown</code>: Not disclosed or not applicable.</li>
  </ul>

  <p>This field may aid in compliance (e.g., export documentation), freight planning, or market segmentation.</p>

</details>

### `export_eligibility_documentation`
- **Data type**: `enum` (multi-select allowed)
- **Valid values**: An enumerated list representing the types of export documentation available for the hay. Options include `[ phytosanitary certificate | fumigation certificate | certificate of origin | weed-free declaration | none | unknown ]`.

<details>
  <summary>More about <code>export_eligibility_documentation</code></summary>

  <p>This field identifies the export-related documentation available for the hay. Such documentation may be required by importing countries, states, or agencies to ensure compliance with quarantine laws, invasive species control, or import regulations.</p>

  <p>Valid options include:</p>
  
  <ul>
    <li><code>phytosanitary certificate</code>: Official document verifying that the hay is free from regulated pests and meets the import requirements of the destination country.</li>
    <li><code>fumigation certificate</code>: Confirms the hay has been treated with a fumigant to control pests or pathogens prior to shipment.</li>
    <li><code>certificate of origin</code>: States the country where the hay was produced, often required for trade preference or compliance verification.</li>
    <li><code>weed-free declaration</code>: Indicates that the hay has been certified free of noxious weeds according to applicable regional or international standards.</li>
    <li><code>none</code>: No export documentation is provided with this hay.</li>
    <li><code>unknown</code>: The documentation status is not known or not disclosed by the seller.</li>
  </ul>

  <p>This field supports international trade, reduces risk of shipment rejection, and helps buyers comply with regulatory requirements in their jurisdiction.</p>

</details>

## In-season crop management

This section documents how the hay crop was managed during the growing season — including cutting strategy, weed and pest management, and other contextual information such as weather stresses or field notes. These details help buyers and agronomists evaluate how active crop management may have influenced the resulting forage quality, consistency, and marketability.

### `growth_conditions_notes`
- **Data type**: `string`
- **Valid values**: A free-text string of up to 500 characters describing notable growing conditions affecting the hay crop.

<details>
  <summary>More about <code>growth_conditions_notes</code></summary>

  <p>This optional field allows the grower or seller to describe notable growing conditions, such as drought, flooding, hail, heat stress, or other environmental factors that may have impacted the hay crop.</p>

  <p>Because such conditions are unpredictable and varied, a free-text format is used here to allow flexibility in reporting.</p>

  <p>Example entries:</p>
  <ul>
    <li><code>Light drought stress during early growth; recovered by late season</code></li>
    <li><code>Localized hail damage in May</code></li>
    <li><code>Flooded low areas did not contribute to harvest</code></li>
  </ul>

  <p>This field is optional but may support transparency in high-trust markets or export documentation.</p>

</details>

### `weed_pressure_observed`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ none | low | moderate | high | unknown ], representing the observed level of weed presence in the field.

<details>
  <summary>More about <code>weed_pressure_observed</code></summary>

  <p>This field estimates the level of weed presence in the field during the growing season. It helps buyers assess forage purity, feeding suitability, and compliance with programs that restrict noxious or invasive species.</p>

  <ul>
    <li><code>none</code>: No visible weed pressure; stand appears clean and uniform.</li>
    <li><code>low</code>: Minor weed presence; unlikely to affect palatability or marketability.</li>
    <li><code>moderate</code>: Noticeable weed presence; may influence feed value or buyer preference.</li>
    <li><code>high</code>: Significant weed presence; likely to reduce market value or trigger restrictions.</li>
    <li><code>unknown</code>: Seller does not know or declined to report.</li>
  </ul>

  <p>This field supports transparency in quality assessment and may inform eligibility for "certified weed free" programs.</p>

</details>

### `hay_herbicide_treated`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether herbicides were applied to the hay field during the growing season.

<details>
  <summary>More about <code>hay_herbicide_treated</code></summary>

  <p>This field discloses whether herbicides were applied to the source field(s) during the growing season of the hay crop. Herbicide treatment may influence weed pressure, forage purity, and potential chemical residues.</p>

  <p>A value of <code>true</code> indicates that herbicides were used, <code>false</code> means they were not, and <code>unknown</code> signifies the seller does not know or does not wish to disclose.</p>

  <p>This information is relevant for buyers concerned with chemical usage, organic compliance, or potential carryover effects in sensitive livestock species.</p>

</details>

### `pest_pressure_observed`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ none | low | moderate | high | unknown ], representing the level of pest pressure observed during the growing season.

<details>
  <summary>More about <code>pest_pressure_observed</code></summary>

  <p>This field reports the level of pest pressure observed during the growing season. Examples of pests include aphids, armyworms, leafhoppers, and weevils.</p>

  <ul>
    <li><code>none</code>: No notable pest activity occurred.</li>
    <li><code>low</code>: Minor pest presence; little or no impact on crop quality or yield.</li>
    <li><code>moderate</code>: Noticeable pest presence; some impact on leaf loss, yield, or quality.</li>
    <li><code>high</code>: Major pest infestation likely to affect quality or marketability.</li>
    <li><code>unknown</code>: Seller does not know or declined to report.</li>
  </ul>

  <p>This field helps inform forage quality evaluation and detect risk factors that may affect feed value or storage.</p>

</details>

### `hay_pesticide_treated`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether pesticides (excluding herbicides) were applied to the hay crop.

<details>
  <summary>More about <code>hay_pesticide_treated</code></summary>

  <p>This field discloses whether pesticides (excluding herbicides) — such as insecticides, fungicides, or miticides — were applied to the hay crop during its growing season.</p>

  <p>A value of <code>true</code> indicates that one or more pesticide treatments were applied. A value of <code>false</code> means no such treatments were used. Use <code>unknown</code> if the seller does not know or does not wish to disclose this information.</p>

  <p>This field is important for buyers managing pesticide sensitivity in livestock, seeking organic compliance, or exporting to jurisdictions with residue restrictions.</p>

</details>

### `hay_preservative_applied`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether a preservative was applied to the hay during harvest or storage.

<details>
  <summary>More about <code>hay_preservative_applied</code></summary>

  <p>This field indicates whether a preservative — such as propionic acid or a similar compound — was applied to the hay during harvest or storage. Preservatives are commonly used to inhibit mold growth and improve the storability of hay baled at higher moisture levels.</p>

  <p>A value of <code>true</code> indicates a preservative was applied, <code>false</code> means no preservative was used, and <code>unknown</code> indicates that the seller does not know or is unwilling to disclose this information.</p>

  <p>Buyers may use this information when evaluating hay for suitability in feeding programs for sensitive livestock or for meeting specific storage or handling protocols.</p>

</details>

### `hay_coloring_agent_used`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether a coloring agent was applied to the hay for cosmetic or marketing purposes.

<details>
  <summary>More about <code>hay_coloring_agent_used</code></summary>

  <p>This field indicates whether a coloring agent was applied to the hay, typically for cosmetic or marketing purposes. Coloring agents are sometimes used to enhance the visual appeal of hay, especially when sun-bleaching or rain damage has occurred post-harvest.</p>

  <p>A value of <code>true</code> indicates that a coloring agent was used, <code>false</code> means no such agent was applied, and <code>unknown</code> indicates that the seller does not know or is unwilling to disclose this information.</p>

  <p>While coloring agents do not alter the nutritional value of the forage, they may affect buyer perception or suitability for certain markets, particularly those emphasizing natural appearance or minimal treatment.</p>

</details>

### `cutting_regimen_usual`
- **Data type**: `int`
- **Valid values**: A positive integer representing the typical number of hay cuttings per year for this field or stand.

<details>
  <summary>More about <code>cutting_regimen_usual</code></summary>

  <p>This field represents the grower’s customary number of hay cuttings per growing season, based on long-term practice with this stand or forage type.</p>

  <p>For example, a field that consistently yields three cuttings per year would be recorded as <code>3</code>. This field reflects normal management, not necessarily the number of cuttings in the year of the current hay offering.</p>

  <p>This value supports agronomic profiling and can help buyers understand harvest frequency, forage regrowth characteristics, and climate- or species-related constraints.</p>

</details>

### `cutting_stage_target`
- **Data type**: `string` or `enum`
- **Valid values**: An enumerated value: [ early vegetative | late vegetative | early bud | full bud | early bloom | full bloom | boot stage | heading | other | unknown ], representing the growth stage at which the grower typically aims to cut hay for optimal quality and yield.

<details>
  <summary>More about <code>cutting_stage_target</code></summary>

  <p>This field identifies the growth stage at which the grower typically aims to cut hay for optimal quality and yield. Growth stage at cutting is a major determinant of forage digestibility, protein content, and fiber levels.</p>

  <p>Examples include:</p>
  
  <ul>
    <li><code>early bud</code> – Alfalfa cut when first buds appear; preferred for dairy-grade forage</li>
    <li><code>boot stage</code> – Grasses cut when seed head is still enclosed; balances yield and quality</li>
    <li><code>full bloom</code> – Often cut here for seed production or lower-cost forage</li>
  </ul>

  <p>This is a grower-reported target, not a measurement of actual maturity at the time of the current harvest. The actual harvest maturity is captured separately in <code>stand_maturity_at_harvest</code>.</p>

</details>

## Harvest-level data

This section documents key facts about the harvest event or events from which the hay was produced. It includes cutting number, harvest dates, field yield, and average bale weight — along with indicators of harvest-specific practices such as conditioning. These fields provide crucial context for traceability, logistics, and quality interpretation, especially when evaluating consistency across lots, seasons, or producers. Accurate reporting of this data supports both market transparency and informed decision-making by buyers and nutritionists.

### `harvest_date_start`
- **Data type**: `datetime`
- **Valid values**: A date in YYYYMMDD format representing the commencement date of the harvest for this hay. Use double-zero formatting for unknown day or month, if applicable.

<details>
  <summary>More about <code>harvest_date_start</code></summary>

  <p>Mowing is generally the first step in harvesting hay and thus represents the commencement of a specific harvest. Identifying the harvest start date informs the consumer as to the age of the hay and season of the harvest. This information may also be useful in ascertaining local weather conditions for the harvest.</p>

  <p>This note applies both to this field and to the <code>harvest_date_end</code> field. The seller may lack specific knowledge of harvest start and end dates and only be able to estimate these dates. A protocol for using estimated dates is feasible through the use of double-zero values for day of month or even month of year. A double zero in the day field would mean that the seller is confident as to the month of the applicable harvest date but not the day. Double zeroes in both the day and month places would mean the seller is confident of the year of harvest but neither the month nor day.</p>

</details>
  
### `harvest_date_end`
- **Data type**: `datetime`
- **Valid values**: A date in YYYYMMDD format representing the conclusion date of the harvest for this hay. Use double-zero formatting for unknown day or month, if applicable.

<details>
  <summary>More about <code>harvest_date_end</code></summary>

  <p>This field captures the end of the harvest window for the hay in question. It may be the same as, but not earlier than, the <code>harvest_date_start</code>. For traceability and quality control, this date is particularly important when evaluating single-lot definitions.</p>

  <p>According to the current working definition of a hay lot, if <code>hay_single_lot</code> is <code>true</code>, then the harvest period must not exceed 48 hours. Therefore, the difference in days between <code>harvest_date_start</code> and <code>harvest_date_end</code> must be two or fewer.</p>

  <p>Systems implementing this standard should validate that the harvest end date adheres to this rule whenever single-lot traceability is claimed.</p>

</details>

### `hay_cutting`
- **Data type**: `int`
- **Valid values**: A non-negative integer representing which cutting of the harvest season produced this hay (e.g., 1 for first cut, 2 for second cut). Enter 0 if unknown.

<details>
  <summary>More about <code>hay_cutting</code></summary>

  <p>The cutting number provides important context for interpreting hay quality, maturity, and nutritional content. Earlier cuttings (e.g., first or second) often yield higher fiber and lower protein, while later cuttings may offer greater digestibility and nutrient density, depending on forage species and environmental conditions.</p>

  <p>This field supports buyers and nutritionists in assessing the relative quality and expected use of the hay. While most growers produce between one and four cuttings per season, high-intensity systems in warm climates may support more.</p>

  <p>If the cutting number is unknown or uncertain, a value of <code>0</code> should be entered. Systems may use this to suppress or flag the cutting in quality analysis models.</p>

</details>

### `baler_moisture_average`
- **Data type**: `float`
- **Valid values**: A decimal value (e.g., `14.5`) representing the average hay moisture percentage measured by baling equipment at the time of harvest.

<details>
  <summary>More about <code>baler_moisture_average</code></summary>

  <p>This field records the average moisture content of the hay as measured by onboard baler sensors during harvest. Moisture content is expressed as a percentage on a wet basis (i.e., total weight including water).</p>

  <p>Average moisture level is critical for assessing storability and spoilage risk. Values above safe thresholds (e.g., 18%) may require preservatives or accelerated drying before storage.</p>

  <p>If no baler moisture data is available, omit this field. Systems should treat this field as optional and informational.</p>

</details>

### `baler_moisture_high`
- **Data type**: `float`
- **Valid values**: A decimal value (e.g., `18.9`) representing the highest moisture content recorded by the baler during harvest.

<details>
  <summary>More about <code>baler_moisture_high</code></summary>

  <p>This field captures the maximum observed hay moisture value recorded by baling equipment sensors at harvest time. High moisture spots can indicate risk areas for mold development or internal heating in storage.</p>

  <p>Buyers concerned with consistency or sensitive livestock may use this data to evaluate overall lot stability. This field is optional and complements <code>baler_moisture_average</code>.</p>

</details>

### `hay_conditioned`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether the hay was mechanically conditioned during harvest.

<details>
  <summary>More about <code>hay_conditioned</code></summary>

  <p>This field indicates whether the hay was conditioned during harvest. Conditioning is a mechanical process that crimps or crushes the forage stems to accelerate drying, reducing the time hay lies in the field and thereby lowering the risk of weather damage and nutrient loss.</p>

  <p>A value of <code>true</code> means the hay was conditioned, <code>false</code> means it was not, and <code>unknown</code> indicates the seller does not know or is unwilling to disclose.</p>

  <p>Conditioning is common in high-moisture environments or where rapid drying is necessary to preserve quality.</p>

</details>

### `bale_weight_intended`
- **Data type**: `int`
- **Valid values**: A positive integer representing the intended average bale weight, in units specified by the `bale_weight_units` field.

<details>
  <summary>More about <code>bale_weight_intended</code></summary>

  <p>This field captures the grower’s target bale weight as configured on the baler or specified in harvest planning. It reflects production goals, logistics optimization, and buyer expectations.</p>

  <p>Use whole numbers only. Units — either <code>kilograms</code> or <code>pounds</code> — must be defined in the associated <code>bale_weight_units</code> field.</p>

  <p>Enter the value as an average across all bales associated with the product definition. If bale weights vary significantly, this value may be misleading and should be qualified by selecting <code>Grower estimate – disparate bales</code> in the <code>bale_weight_assessment_method</code> field.</p>

  <p>Systems implementing this standard may apply validation to flag improbable weights and ensure consistency between declared unit and value.</p>

</details>

### `average_bale_weight`
- **Data type**: `int`
- **Valid values**: A positive integer representing the actual or estimated average bale weight, expressed in the units defined by `bale_weight_units`.

<details>
  <summary>More about <code>average_bale_weight</code></summary>

  <p>This field captures the average weight of individual bales within the hay lot being offered. It may reflect direct measurements, truckload calculations, baler settings, or visual estimation — as indicated in the <code>bale_weight_assessment_method</code> field.</p>

  <p>Provide a whole-number value corresponding to the typical bale weight across the lot. This helps buyers assess product consistency, shipping requirements, and stacking logistics.</p>

  <p>Interpret this field in conjunction with:</p>

  <ul>
    <li><code>bale_weight_units</code> – Identifies the unit of measure (e.g., pounds, kilograms)</li>
    <li><code>bale_weight_assessment_method</code> – Describes how the value was derived</li>
  </ul>

  <p>Examples:</p>

  <ul>
    <li>If bales average approximately 60 pounds each, enter <code>60</code>.</li>
    <li>If bales weigh about 27 kilograms, enter <code>27</code> and ensure <code>bale_weight_units</code> is set to <code>kilograms</code>.</li>
  </ul>

  <p>Systems implementing this specification may use this field to compute lot totals or shipping weights, or to validate consistency with declared totals.</p>

</details>

### `bale_weight_assessment_method`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Truckload average | Explicit weight | Baler target | Grower estimate—uniform bales | Grower estimate—disparate bales ]`, representing the method used to determine reported bale weight.

<details>
  <summary>More about <code>bale_weight_assessment_method</code></summary>

  <p>This field specifies the method used to determine the bale weight reported in either <code>bale_weight_intended</code> or <code>average_bale_weight</code>. It offers transparency into how the weight was derived, helping buyers assess data reliability and consistency.</p>

  <ul>
    <li><code>Truckload average</code>: Derived by dividing total load weight by number of bales, using truck scale data.</li>
    <li><code>Explicit weight</code>: Based on actual weights from individual bale measurements using a certified scale.</li>
    <li><code>Baler target</code>: Reflects the programmed weight setting of the baler; useful when scale data is unavailable.</li>
    <li><code>Grower estimate—uniform bales</code>: Visual or experiential estimate with relatively consistent bale size.</li>
    <li><code>Grower estimate—disparate bales</code>: Visual or experiential estimate where bale size varies significantly.</li>
  </ul>

  <p>Providing this metadata helps ensure informed decision-making and encourages consistent reporting practices across sellers and regions.</p>

</details>

### `bale_count`
- **Data type**: `int`
- **Valid values**: A positive integer representing the total number of bales produced from this lot.

<details>
  <summary>More about <code>bale_count</code></summary>

  <p>This field records the total number of bales created during the harvest event. It enables calculation of total lot mass when paired with <code>average_bale_weight</code>, and helps with planning for shipping, inventory, and storage.</p>

  <p>Counts should reflect marketable bales only and exclude spoiled or rejected units where possible.</p>

</details>

### `source_field_yield`
- **Data type**: `int`
- **Valid values**: An integer representing the magnitude of the yield from the source field(s) for this hay, rounded to the nearest whole number, whether in metric, long, or short tons.

Use the field `source_field_yield_units` to specify the unit of measure for this magnitude.

<details>
  <summary>More about <code>source_field_yield</code></summary>

  <p>Yield is defined here as the product of the total number of bales and their average weight. This metric offers a quantifiable expression of field productivity and helps downstream users assess supply availability, compare harvests, or normalize quality measures by output volume.</p>

  <p>Yield may be calculated at the field, lot, or operation level, but should be associated with the source field(s) for this hay. Systems implementing this specification may prompt for supporting values — such as bale count and average bale weight — to assist the user in estimating yield accurately.</p>

</details>

### `source_field_yield_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ metric tons | British (long) tons | U.S. (short) tons ], representing the unit of measurement used for yield reporting.

<details>
  <summary>More about <code>source_field_yield_units</code></summary>

  <p>This field specifies the unit of measure used to express the yield reported in the <code>source_field_yield</code> field. Standardizing units of measure is essential for data consistency across geographies and reporting systems.</p>

  <p>
    <strong>Metric tons</strong> are equal to 1,000 kilograms (approximately 2,204.62 pounds).  
    <strong>British (long) tons</strong> are equal to 2,240 pounds.  
    <strong>U.S. (short) tons</strong> are equal to 2,000 pounds.
  </p>

  <p>Implementations should enforce alignment between the numeric yield and this unit selection to ensure that conversions and aggregations across records are reliable.</p>
</details>

## Weather exposure and damage

This section discloses whether the hay was exposed to adverse weather events during two key periods: while lying in the windrow (after mowing and before baling) and after baling (during handling or storage). Weather-related exposure can significantly affect visual quality, nutritional value, and storability. By disclosing both specific weather events and overall impact assessments, this section enhances buyer confidence and supports accurate market representation.

Fields in this section cover both stages:

- **Windrow-stage exposure**: Rain, snow, sleet, hail, fog, and dewfall
- **Baled-stage exposure**: Rain, snow, sleet, hail, and moisture-related damage (e.g., fog or condensation)
- **Summary assessments**: Overall severity of damage at each stage

### `weather_damage_windrow_rain`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced rainfall while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_rain</code></summary>

  <p>This field discloses whether the hay was exposed to rainfall while lying in the windrow. Rain during this stage of harvest can leach nutrients, increase the risk of mold, and reduce overall forage quality.</p>

  <p>Use <code>true</code> to indicate that rainfall occurred while the hay was in the windrow; <code>false</code> to affirm that no rain fell on the windrow; and <code>unknown</code> if the seller does not know whether rainfall occurred.</p>

  <p>This information is especially important to buyers concerned with hay color, leaf retention, and feed value.</p>

</details>

### `weather_damage_windrow_snow`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced snowfall while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_snow</code></summary>

  <p>This field discloses whether the hay was exposed to snowfall while lying in the windrow. Snowfall can slow drying, increase moisture content, and contribute to microbial degradation if not properly managed during harvest.</p>

  <p>Use <code>true</code> to indicate that snow fell on the hay while in the windrow; <code>false</code> to affirm that no snow was received; and <code>unknown</code> if the seller is uncertain whether snowfall occurred.</p>

  <p>Snow exposure during curing is a key concern in colder climates and may influence storage recommendations and marketability.</p>

</details>

### `weather_damage_windrow_sleet`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced sleet while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_sleet</code></summary>

  <p>This field discloses whether the hay was exposed to sleet while lying in the windrow. Sleet — a mixture of rain and ice — can affect drying time, increase leaf loss, and contribute to weathering, potentially diminishing hay quality.</p>

  <p>Use <code>true</code> to indicate that sleet fell on the hay in the windrow; <code>false</code> to affirm that no sleet was received; and <code>unknown</code> if the seller is uncertain whether sleet occurred.</p>

  <p>Even short periods of sleet exposure can affect the physical and nutritional characteristics of hay, especially when combined with freezing temperatures or extended curing periods.</p>

</details>

### `weather_damage_windrow_hail`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced hail while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_hail</code></summary>

  <p>This field discloses whether the hay was exposed to hail while lying in the windrow. Hail can physically damage forage by shattering leaves, bruising stems, or embedding ice into the material — all of which can reduce forage quality and palatability.</p>

  <p>Use <code>true</code> if hail was received; <code>false</code> to affirm that no hail fell; and <code>unknown</code> if the seller is uncertain about hail exposure during the windrow stage.</p>

  <p>Even localized hail events can affect hay in specific parts of a field, so sellers should answer this question based on their best available knowledge or observation.</p>

</details>

### `weather_damage_windrow_fog`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced fog while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_fog</code></summary>

  <p>This field discloses whether the hay was exposed to fog while lying in the windrow. Fog can contribute to prolonged moisture retention, delayed drying, and increased risk of mold growth or spontaneous heating, especially if the hay is baled before it is fully cured.</p>

  <p>Use <code>true</code> if fog was observed or known to have affected the windrow; <code>false</code> if no fog occurred; and <code>unknown</code> if the seller lacks information about fog conditions during the windrow stage.</p>

  <p>Fog-related moisture is especially critical in regions or seasons with limited drying windows or high humidity. Sellers should respond based on field observation or reliable local weather data.</p>

</details>

### `weather_damage_windrow_dewfall`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced heavy dewfall while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_dewfall</code></summary>

  <p>This field indicates whether the hay experienced heavy dewfall while lying in the windrow. Dew can reintroduce moisture to partially dried forage, delaying the curing process and increasing the risk of microbial activity, mold development, or heat damage if baled prematurely.</p>

  <p>Use <code>true</code> if significant dewfall was observed on the windrow; <code>false</code> if the windrow avoided heavy dewfall; and <code>unknown</code> if the seller lacks adequate knowledge to assess dew exposure.</p>

  <p>Heavy dew is more common during certain weather patterns or geographic regions. Accurate reporting helps downstream buyers assess potential quality concerns related to post-mowing moisture events.</p>

</details>

### `weather_damage_windrow_assessment`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ none | minor | modest | substantial | unknown ], representing the seller’s qualitative assessment of weather-related damage to the hay while in the windrow.

<details>
  <summary>More about <code>weather_damage_windrow_assessment</code></summary>

  <p>This field allows the seller to provide a summary-level assessment of the weather-related damage the hay may have incurred while lying in the windrow. It is especially useful when specific precipitation or moisture events have been disclosed in prior fields but require contextual interpretation.</p>

  <p>Use <code>none</code> if the hay experienced no perceptible damage while in the windrow; <code>minor</code> if slight discoloration or nutrient loss occurred; <code>modest</code> if moderate quality reduction was observed; and <code>substantial</code> if hay quality was significantly compromised. Choose <code>unknown</code> if the seller lacks enough information to make an informed judgment.</p>

  <p>This qualitative field supplements quantitative or binary data with human judgment, offering a useful signal to buyers in the absence of lab analysis.</p>

</details>

### `weather_damage_baled_rain`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay received rainfall after it was baled.

<details>
  <summary>More about <code>weather_damage_baled_rain</code></summary>

  <p>This field may be implemented as an enumerated data type, with <code>true</code> representing the seller's disclosure that this hay received rainfall once baled, <code>false</code> the seller's affirmation that no rain fell on the bales, and <code>unknown</code> the seller's disclosure that he has no knowledge of whether the bales received rainfall.</p>

  <p>Rainfall after baling can significantly affect hay quality by introducing mold risk, lowering palatability, and increasing spoilage potential during storage. Accurate disclosure enhances transparency and allows buyers to assess storage and feeding implications.</p>

</details>

### `weather_damage_baled_snow`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay received snowfall after it was baled.

<details>
  <summary>More about <code>weather_damage_baled_snow</code></summary>

  <p>This field may be implemented as an enumerated data type, with <code>true</code> representing the seller's disclosure that this hay received snow once baled, <code>false</code> the seller's affirmation that no snow fell on the bales, and <code>unknown</code> the seller's disclosure that he has no knowledge of whether the bales received snowfall.</p>

  <p>Snow accumulation on baled hay may contribute to external moisture exposure, leading to spoilage or mold growth, especially during freeze-thaw cycles. Disclosure of snow exposure informs buyers of potential quality degradation and storage risks.</p>

</details>

### `weather_damage_baled_sleet`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay received sleet after it was baled.

<details>
  <summary>More about <code>weather_damage_baled_sleet</code></summary>

  <p>This field may be implemented as an enumerated data type, with <code>true</code> representing the seller's disclosure that this hay received sleet once baled, <code>false</code> the seller's affirmation that no sleet fell on the bales, and <code>unknown</code> the seller's disclosure that he has no knowledge of whether the bales received sleet.</p>

  <p>Sleet can cause surface moisture and freezing damage to baled hay, potentially compromising bale integrity, increasing spoilage risk, or making handling more difficult. Disclosure of sleet exposure provides insight into hay condition and post-harvest weather vulnerability.</p>

</details>

### `weather_damage_baled_hail`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay received hail after it was baled.

<details>
  <summary>More about <code>weather_damage_baled_hail</code></summary>

  <p>This field may be implemented as an enumerated data type, with <code>true</code> representing the seller's disclosure that this hay received hail once baled, <code>false</code> the seller's affirmation that no hail fell on the bales, and <code>unknown</code> the seller's disclosure that he has no knowledge of whether the bales received hail.</p>

  <p>Hail can damage the outer surfaces of hay bales, potentially compromising their structural integrity or allowing for increased moisture penetration and spoilage. While not common, hail exposure may affect appearance, palatability, or storage characteristics.</p>

</details>

### `weather_damage_baled_moisture`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ true | false | unknown ], representing whether the hay experienced excessive moisture (e.g., fog or dew) after it was baled.

<details>
  <summary>More about <code>weather_damage_baled_moisture</code></summary>

  <p>This field may be implemented as an enumerated data type, with <code>true</code> representing the seller's disclosure that this hay experienced fog, heavy dewfall, or another source of excessive moisture once baled, <code>false</code> the seller's affirmation that no such phenomena affected the bales, and <code>unknown</code> the seller's disclosure that he has no knowledge of whether fog, heavy dewfall, or any other source of excessive moisture affected the bales.</p>

  <p>Excessive moisture after baling can lead to spoilage, mold growth, or heating within the bale, which may reduce forage quality and pose health risks to livestock. This field allows sellers to disclose potential post-baling moisture exposure that could affect hay safety or shelf life.</p>

</details>

### `weather_damage_baled_assessment`
- **Data type**: `enum`
-**Valid values**: An enumerated value: [ None | Minor | Modest | Substantial | Unknown ], representing the seller’s assessment of post-baling weather-related damage severity.

<details>
  <summary>More about <code>weather_damage_baled_assessment</code></summary>

  <p>This field allows the seller to disclose an overall assessment of weather-related damage to the hay that occurred after baling. This includes any deterioration caused by exposure to rain, snow, sleet, fog, dewfall, or other sources of moisture or environmental stress while the hay was in bale form.</p>

  <p>The enumerated values indicate the severity of the observed or suspected damage:

  <ul>
    <li><code>None</code>: No post-baling weather damage is known or suspected.</li>
    <li><code>Minor</code>: Slight exposure or damage with minimal impact on hay quality.</li>
    <li><code>Modest</code>: Noticeable damage that may affect appearance, smell, or shelf life.</li>
    <li><code>Substantial</code>: Significant degradation, potentially affecting nutritional value or usability.</li>
    <li><code>Unknown</code>: The seller cannot assess the level of post-baling weather damage.</li>
  </ul>

  </p>

  <p>This field provides a summary judgment that complements individual weather exposure fields and supports transparency in product condition reporting.</p>

</details>

## Hay packaging

This section describes the physical form in which the hay is currently packaged for sale or shipment. It includes bale dimensions, binding material, compression method, and other packaging details that affect storage, transport, handling, and customer preferences.

Packaging specifications may differ from original harvest conditions — particularly in cases where hay has been rebaled or processed after the initial cutting. Buyers rely on this data to assess compatibility with feeding systems, freight capacity, and regulatory or market requirements.

**Note:** Some hay may be reprocessed or rebaled after the initial harvest. Fields in this section (including weight, shape, and compression) describe the hay as currently packaged for sale or shipment — which may differ from the original harvest form.

### `hay_packaging_history`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ original | rebaled | repackaged | unknown ], representing the packaging status and history of the hay.

<details>
  <summary>More about <code>hay_packaging_history</code></summary>

  <p>This field describes whether the hay is in its original bale form or has undergone repackaging. Repackaging may include unrolling and re-baling, compressing for export, or resizing for specific markets.</p>

  <ul>
    <li><code>original</code>: Hay is in the form in which it was first baled.</li>
    <li><code>rebaled</code>: Hay was originally baled, then unrolled and baled again.</li>
    <li><code>repackaged</code>: Hay was processed into a different format (e.g., compressed, shrink-wrapped).</li>
    <li><code>unknown</code>: Packaging history is unclear or not disclosed.</li>
  </ul>

  <p>This field supports traceability and helps buyers assess potential quality or handling concerns related to reprocessing.</p>

</details>

### `bale_weight_intended_repackaged`
- **Data type**: `int`
- **Valid values**: A positive whole number representing the intended weight (in units defined by `bale_weight_units`) of each bale in its final, repackaged form.

<details>
  <summary>More about <code>bale_weight_intended_repackaged</code></summary>

  <p>This field applies only when hay has been re-baled or repackaged after the original harvest. It specifies the <strong>target weight of the new bales</strong>, such as when large round bales are broken down and re-formed into smaller square bales for transport or sale.</p>

  <p>This value is expressed in the same units as <code>bale_weight_units</code> (e.g., pounds or kilograms). It reflects the intended packaging outcome and may differ substantially from the original <code>bale_weight_intended</code> captured at harvest.</p>

  <p>Use this field only if <code>hay_packaging_history</code> includes values such as <code>rebaled</code> or <code>repackaged</code>. When applicable, this field provides important clarity for buyers and logistics providers, especially in export or high-volume contexts.</p>

  <p>System interfaces may optionally validate this field in relation to <code>bale_shape</code>, <code>bale_dimension_*</code>, or <code>bale_binding</code> fields to ensure internal consistency.</p>

</details>

### `bale_weight_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ kilograms | pounds ], representing the unit of measurement used for bale weight fields.

<details>
  <summary>More about <code>bale_weight_units</code></summary>

  <p>This field specifies the unit of measurement used in the <code>bale_weight_intended</code> and potentially other bale weight fields. Most systems should standardize internally on one unit, but external presentation may vary by user preference or region.</p>

  <p>Providing a clear unit prevents misinterpretation, especially when converting or comparing listings across geographies.</p>

</details>

### `bale_binding_material`
- **Data type**: `enum`
- **Valid values**: An enumerated value: [ twine | net wrap | wire | plastic strap | none | unknown ], representing the material used to bind the bale.

<details>
  <summary>More about <code>bale_binding_material</code></summary>

  <p>Records the primary material used to bind or wrap the bale for storage and handling. Material type affects bale durability, safety, and disposal requirements.</p>

  <ul>
    <li><code>twine</code>: Natural (e.g., sisal) or synthetic (e.g., polypropylene) twine.</li>
    <li><code>net wrap</code>: Plastic or polymer netting, typically used on round bales.</li>
    <li><code>wire</code>: Steel or galvanized wire, often used for high-density rectangular bales.</li>
    <li><code>plastic strap</code>: Plastic strapping commonly used on compressed or export bales.</li>
    <li><code>none</code>: No external binding applied to the bale.</li>
    <li><code>unknown</code>: Binding material is not known or not disclosed.</li>
  </ul>

</details>

### `bale_binding_details`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ small two-strand | small three-strand | large 3x3x8 | large 3x4x8 | large 4x4x8 | round twine | round net wrap | round plastic wrap | other ]`, representing the bale’s size and binding configuration.

<details>
  <summary>More about <code>bale_binding_details</code></summary>

  <p>This field captures the size, shape, and basic binding configuration of the bale. It is independent of the binding material (e.g., wire or twine), which is recorded separately in <code>bale_binding</code>.</p>

  <ul>
    <li><code>small two-strand</code> – Small rectangular bale tied with two strands of twine or wire.</li>
    <li><code>small three-strand</code> – Slightly larger small bale tied with three strands.</li>
    <li><code>large 3x3x8</code> – Large square bale approximately 3'×3'×8'.</li>
    <li><code>large 3x4x8</code> – Large square bale approximately 3'×4'×8'.</li>
    <li><code>large 4x4x8</code> – Extra-large square bale approximately 4'×4'×8'.</li>
    <li><code>round twine</code> – Round bale bound with twine.</li>
    <li><code>round net wrap</code> – Round bale secured with net wrap.</li>
    <li><code>round plastic wrap</code> – Round bale sealed in plastic, often for haylage.</li>
    <li><code>other</code> – Non-standard or specialized bale types.</li>
  </ul>

  <p>Binding material (twine, wire, net, plastic) should be separately recorded in <code>bale_binding</code>.</p>

</details>

### `hay_compression`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ standard | mid-compressed | fully compressed | unknown ]`, representing the extent to which the hay bale has been mechanically compressed for storage or transport.

<details>
  <summary>More about <code>hay_compression</code></summary>

  <p>This field describes whether and to what extent the bale has been mechanically compressed to reduce its volume. Compressed hay is often produced for export or for storage efficiency.</p>

  <ul>
    <li><code>standard</code>: Bales are not compressed beyond what occurs during baling.</li>
    <li><code>mid-compressed</code>: Bales have undergone moderate compression (e.g., for container loading).</li>
    <li><code>fully compressed</code>: Bales are significantly compressed using hydraulic or mechanical means.</li>
    <li><code>unknown</code>: Compression status is not known or not disclosed.</li>
  </ul>

  <p>This field is particularly useful in international trade and for evaluating bale density relative to storage or freight constraints.</p>

</details>

### `bale_shape`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ round | rectangular | other ]`, representing the geometric shape of the hay bale.

<details>
  <summary>More about <code>bale_shape</code></summary>

  <p>This field records the geometric shape of the bale. Bale shape affects equipment compatibility, stacking, and handling procedures.</p>

  <ul>
    <li><code>round</code>: Cylindrical bale shape, often larger and heavier.</li>
    <li><code>rectangular</code>: Includes small square, mid-size, and large square bales.</li>
    <li><code>other</code>: Includes cubes, wafers, or non-standard formats.</li>
  </ul>

  <p>Shape selection may be influenced by market expectations, shipping constraints, or equipment availability.</p>

</details>

### `bale_dimension_width`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the width of the bale, in the units specified by `bale_dimension_units`.

<details>
  <summary>More about <code>bale_dimension_width</code></summary>

  <p>Enter the bale’s width (short side of the rectangular face, or diameter for round bales). Values should be rounded to the nearest 0.1 unit (e.g., 3.5 feet).</p>

  <p>This field helps buyers assess compatibility with handling equipment and loading systems.</p>

</details>

### `bale_dimension_height`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the height of the bale, in the units specified by `bale_dimension_units`.

<details>
  <summary>More about <code>bale_dimension_height</code></summary>

  <p>Enter the bale’s height (long side of the rectangular face when standing, or vertical axis if round). Round to the nearest 0.1 unit.</p>

  <p>This field is important for planning stacking and clearance requirements in storage facilities.</p>

</details>

### `bale_dimension_length`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the length of the bale, in the units specified by `bale_dimension_units`.

<details>
  <summary>More about <code>bale_dimension_length</code></summary>

  <p>Enter the bale’s length (longest axis for rectangular bales). Round to the nearest 0.1 unit.</p>

  <p>This measurement aids in evaluating stacking strategies and trailer fit.</p>

</details>

### `bale_dimension_diameter`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the diameter of round bales, in the units specified by `bale_dimension_units`.

<details>
  <summary>More about <code>bale_dimension_diameter</code></summary>

  <p>Use this field only for round bales. Enter the diameter of the cylinder, rounded to the nearest 0.1 unit. For rectangular bales, leave this field blank or exclude it from output.</p>

  <p>Diameter is crucial for modeling bale volume and handling characteristics.</p>

</details>

### `bale_dimension_units`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ inches | centimeters | feet | meters ]`, representing the unit of measurement used for all bale dimensions.

<details>
  <summary>More about <code>bale_dimension_units</code></summary>

  <p>This field specifies the unit of measurement used for the bale dimensions listed above. Consistent units allow for accurate volume, storage, and logistics calculations.</p>

  <ul>
    <li><code>inches</code>: Common in North America for small bales.</li>
    <li><code>centimeters</code>: Metric alternative to inches.</li>
    <li><code>feet</code>: Common for large bales in U.S. agriculture.</li>
    <li><code>meters</code>: Used in international and metric-based systems.</li>
  </ul>

  <p>Implementing systems should support conversion and validation tools based on this field.</p>

</details>

### Notes on Hay Packaging

<details>
  <summary>Cross-field consistency guidance</summary>

  <p>To improve interpretability and reduce conflicting information, systems implementing this standard may consider applying the following cross-field validation logic:</p>

  <ul>
    <li>If <code>hay_packaging_history</code> = <code>rebaled</code> or <code>repackaged</code>, then <code>average_bale_weight</code> and <code>bale_dimension_*</code> fields may differ significantly from typical field-scale values.</li>
    
    <li>If <code>bale_shape</code> = <code>round</code>, then <code>bale_dimension_diameter</code> is expected and <code>bale_dimension_length</code> may be optional or ignored.</li>
    
    <li>If <code>bale_shape</code> = <code>rectangular</code>, then <code>bale_dimension_width</code>, <code>bale_dimension_height</code>, and <code>bale_dimension_length</code> should be present; <code>bale_dimension_diameter</code> should be excluded.</li>
    
    <li>If <code>hay_compression</code> = <code>fully compressed</code>, then <code>bale_binding</code> is likely <code>plastic strap</code> or <code>wire</code> — and bale weight may exceed standard values for the declared shape and dimensions.</li>
  </ul>

  <p>These cross-checks are not absolute rules but may help identify internal inconsistencies in seller submissions and assist in downstream data validation or normalization.</p>

</details>

## Visual and organoleptic qualities

This section describes the physical appearance and sensory characteristics of the hay — including texture, color, odor, and the presence of foreign or undesirable materials. These traits strongly influence buyer perception, animal intake, and marketability, especially when laboratory analysis is unavailable. By documenting visual and organoleptic factors in a structured way, this specification supports consistent grading, transparency, and alignment with the expectations of specialized markets such as equine, export, and organic systems.

<details>
  <summary>Cross-field consistency guidance</summary>

  <ul>
    <li>If <code>organoleptic_factor_moldy</code> = <code>true</code>, then <code>organoleptic_factor_odor</code> is often <code>Moldy</code>.</li>
    <li>If <code>organoleptic_factor_rot</code> = <code>true</code>, then <code>organoleptic_factor_odor</code> may be <code>Sour</code> or <code>Rotten or otherwise foul</code>.</li>
    <li>If <code>foreign_material_weeds</code> = <code>true</code>, buyers may expect <code>certified weed free</code> status to be <code>false</code> in <code>certification_status</code>.</li>
    <li>Fields in this section may also correlate with observed or suspected weather damage — particularly if hay is <code>brown or black</code>, <code>harsh</code> in texture, or <code>moldy</code>.</li>
  </ul>

</details>

### `hay_leafiness`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Very leafy | Leafy | Slightly stemmy | Stemmy ]`, representing the observed leaf-to-stem ratio of the hay based on visual inspection.

<details>
  <summary>More about <code>hay_leafiness</code></summary>

  <p>This field provides a qualitative assessment of the leaf-to-stem ratio in the hay, based on visual observation or standard grading procedures. Leafiness is a key determinant of forage quality, as leaves generally contain more digestible nutrients than stems.</p>

  <p>The classification scheme is adapted from Bates (2007), and the values reflect increasing stem content and decreasing feed quality as one moves from <code>Very leafy</code> to <code>Stemmy</code>.</p>

  <ul>
    <li><code>Very leafy</code>: Dominated by leaves, minimal visible stem.</li>
    <li><code>Leafy</code>: Leafy with some stem presence.</li>
    <li><code>Slightly stemmy</code>: Noticeable stem content, but still a moderate leaf presence.</li>
    <li><code>Stemmy</code>: Predominantly stems, limited leaf material.</li>
  </ul>

  <p>This field can be used to support visual grading and may correlate with laboratory results for digestibility and nutrient density.</p>

</details>

### `hay_texture`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Very soft and pliable | Soft | Slightly harsh | Harsh, brittle ]`, representing the tactile texture of the hay as assessed by physical inspection.

<details>
  <summary>More about <code>hay_texture</code></summary>

  <p>This field captures a tactile assessment of the hay’s texture, reflecting how soft or harsh it feels to the touch. Texture may influence animal intake, especially for more selective livestock like horses or young animals.</p>

  <p>The classification follows the scheme presented on page 6 of Bates (2007), ranging from <code>Very soft and pliable</code>—indicative of early-cut or well-cured hay—to <code>Harsh, brittle</code>, which may reflect overmaturity, poor curing, or weather damage.</p>

  <ul>
    <li><code>Very soft and pliable</code>: Tender and flexible, no harshness.</li>
    <li><code>Soft</code>: Generally smooth, some minor resistance to handling.</li>
    <li><code>Slightly harsh</code>: Noticeable coarseness or rigidity.</li>
    <li><code>Harsh, brittle</code>: Very coarse, easily broken, may include tough stems.</li>
  </ul>

  <p>This qualitative measure complements analytical data and visual characteristics, helping buyers anticipate palatability and usability across animal classes.</p>

</details>

### `hay_color`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Natural green color of crop | Light green | Yellow to slightly brownish | Brown or black ]`, representing the visual color of the hay and serving as an indicator of forage quality and harvest conditions.

<details>
  <summary>More about <code>hay_color</code></summary>

  <p>This field records the dominant color of the hay at the time of sale, which serves as a visual indicator of forage quality, harvest conditions, and storage practices.</p>

  <p>The classification is adapted from page 6 of Bates (2007) and represents a range of common hay appearances:</p>

  <ul>
    <li><code>Natural green color of crop</code>: Bright green, indicating good curing and preservation of nutrients.</li>
    <li><code>Light green</code>: Slight fading, often due to moderate exposure to sunlight or time in storage.</li>
    <li><code>Yellow to slightly brownish</code>: Indicates aging, weathering, or delayed harvest. Nutritional quality may be diminished.</li>
    <li><code>Brown or black</code>: Often the result of rain damage, excessive heating, or mold. May signify reduced palatability or spoilage.</li>
  </ul>

  <p>While subjective, hay color plays a role in buyer perception and is often used alongside analytical data for quality assessment.</p>

</details>

### `organoleptic_factor_odor`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Clean--"crop smell" | Dusty | Moldy | Somewhat sour | Sour | Rotten or otherwise foul ]`, representing the perceived odor of the hay as a sensory indicator of harvest and storage conditions.

<details>
  <summary>More about <code>organoleptic_factor_odor</code></summary>

  <p>This field captures the perceived odor of the hay as detected by human smell. Odor is a key organoleptic (sensory) characteristic and often reflects harvest and storage conditions.</p>

  <p>The classification scheme is adapted from page 6 of Bates (2007) and ranges from desirable to undesirable qualities:</p>

  <ul>
    <li><code>Clean--"crop smell"</code>: Fresh, sweet odor typical of well-cured hay.</li>
    <li><code>Dusty</code>: Dry, musty smell, possibly indicating excessive dust or old material.</li>
    <li><code>Moldy</code>: Odor of mold, typically a sign of spoilage and potential health risk to animals.</li>
    <li><code>Somewhat sour</code>: Slight fermentation scent, possibly from premature baling or partial spoilage.</li>
    <li><code>Sour</code>: Clear sour odor, usually from significant fermentation or improper storage.</li>
    <li><code>Rotten or otherwise foul</code>: Strong, unpleasant smell often due to microbial decay, wet storage, or contamination.</li>
  </ul>

  <p>Odor assessment is inherently subjective but plays an important role in buyer evaluation of forage quality, especially when analytical data is not available.</p>

</details>

### `organoleptic_factor_moldy`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether visible mold is present on the hay based on seller observation.

<details>
  <summary>More about <code>organoleptic_factor_moldy</code></summary>

  <p>This field records whether visible mold is present on the hay, based on the seller's observation. Mold can affect palatability, reduce nutritional value, and pose health risks—particularly respiratory issues—for livestock and handlers.</p>

  <ul>
    <li><code>true</code>: The seller affirms the presence of visible mold on the hay.</li>
    <li><code>false</code>: The seller affirms that no visible mold is present on the hay.</li>
    <li><code>unknown</code>: The seller does not know whether mold is present, or has not inspected the hay closely enough to determine.</li>
  </ul>

  <p>Mold development may result from excessive moisture, delayed baling, or improper storage. Even small amounts of mold may influence hay grading and usability depending on the intended livestock species and sensitivity.</p>

</details>

### `organoleptic_factor_dusty`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether the hay is visibly dusty based on seller observation.
<details>
  <summary>More about <code>organoleptic_factor_dusty</code></summary>

  <p>This field records whether the hay is visibly dusty, based on the seller’s observation. Dustiness can result from soil contamination, excessive handling, or overly dry baling conditions.</p>

  <ul>
    <li><code>true</code>: The seller affirms the presence of visible dust in or on the hay.</li>
    <li><code>false</code>: The seller affirms that the hay is not dusty.</li>
    <li><code>unknown</code>: The seller does not know or has not assessed whether the hay is dusty.</li>
  </ul>

  <p>Dust can reduce palatability, cause respiratory irritation in livestock, and affect visual appeal. The presence or absence of dust is often a key factor in hay quality assessments and buyer decisions.</p>

</details>

### `organoleptic_factor_rot`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether the hay exhibits visible or olfactory signs of rot based on seller observation.

<details>
  <summary>More about <code>organoleptic_factor_rot</code></summary>

  <p>This field records whether the hay exhibits visible or olfactory signs of rot, based on the seller’s observation. Rot may result from baling hay at excessively high moisture, water damage, or poor storage conditions.</p>

  <ul>
    <li><code>true</code>: The seller affirms that some or all of the hay is rotten.</li>
    <li><code>false</code>: The seller affirms that the hay shows no signs of rot.</li>
    <li><code>unknown</code>: The seller does not know or has not assessed whether the hay is rotten.</li>
  </ul>

  <p>Rot can significantly compromise hay quality, posing risks to livestock health and reducing nutritional value. Its disclosure is important for ensuring transparency in hay transactions.</p>

</details>

### `foreign_material_weeds`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether the hay contains visible weed material based on seller observation or knowledge.

<details>
  <summary>More about <code>foreign_material_weeds</code></summary>

  <p>This field indicates whether the hay contains visible weed material, based on the seller’s observation or knowledge. Weeds may reduce the nutritional value of hay, affect palatability, or introduce harmful or noxious plant species into a buyer’s operation.</p>

  <ul>
    <li><code>true</code>: The seller affirms that weed material is present in the hay.</li>
    <li><code>false</code>: The seller affirms that no weed material is present.</li>
    <li><code>unknown</code>: The seller is unsure or has not assessed whether weeds are present in the hay.</li>
  </ul>

  <p>Disclosure of weed presence is especially important when exporting hay or selling to operations with strict feed quality requirements.</p>

</details>

### `foreign_material_burs`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether burs are present in the hay based on seller observation or knowledge.

<details>
  <summary>More about <code>foreign_material_burs</code></summary>

  <p>This field indicates whether the hay contains burs—sharp, spiny plant structures that can be present in certain weeds or grasses. Burs may reduce the desirability and safety of hay, particularly for animals with sensitive mouths or skin, such as horses or show livestock.</p>

  <ul>
    <li><code>true</code>: The seller affirms that burs are present in the hay.</li>
    <li><code>false</code>: The seller affirms that no burs are present in the hay.</li>
    <li><code>unknown</code>: The seller is unsure or has not assessed whether burs are present.</li>
  </ul>

  <p>Buyers may use this information to avoid hay that could cause discomfort, injury, or contamination in feeding systems or animal coats.</p>

</details>

### `foreign_material_insects`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether insects or insect residues are present in the hay based on seller observation or knowledge.

<details>
  <summary>More about <code>foreign_material_insects</code></summary>

  <p>This field indicates whether insect presence or contamination has been observed in the hay. Insects may include live pests, dead insects, or insect remnants such as wings, legs, or webs. Their presence may affect hay palatability, marketability, and compliance with regulatory standards.</p>

  <ul>
    <li><code>true</code>: The seller affirms that insects or insect residues are present in the hay.</li>
    <li><code>false</code>: The seller affirms that no insects or insect residues are present in the hay.</li>
    <li><code>unknown</code>: The seller is unsure or has not assessed whether insects are present.</li>
  </ul>

  <p>Buyers may use this information to evaluate product cleanliness and suitability for particular species or markets with stricter standards (e.g., equine or export). Systems implementing this field may allow for integration with pest identification features in future versions.</p>

</details>

## Storage and handling

This section captures the conditions under which the hay has been stored following baling. Storage environment, surface contact, exposure history, and airflow conditions significantly influence hay quality, shelf life, and susceptibility to spoilage or mold. These fields help buyers understand how well the hay has been protected and whether storage practices align with their quality expectations.

### `final_storage_structure`
- **Data type**: `enum`  
- **Valid values**: An enumerated value: `[ field | tarp-covered | open shed | enclosed barn | unknown ]`, representing the final known type of structure used to store the hay before sale or transfer.

<details>
  <summary>More about <code>final_storage_structure</code></summary>

  <p>Describes the most recent structure used to house or protect the hay before sale or pickup.</p>

  <ul>
    <li><code>field</code>: Stored outdoors with no covering.</li>
    <li><code>tarp-covered</code>: Covered with tarp or plastic sheeting outdoors.</li>
    <li><code>open shed</code>: Stored under a roofed but open or partially enclosed structure.</li>
    <li><code>enclosed barn</code>: Stored in a fully enclosed building.</li>
    <li><code>unknown</code>: Final structure not known or not reported.</li>
  </ul>
</details>

### `final_surface_type`
- **Data type**: `enum`  
- **Valid values**: An enumerated value: `[ ground | pallets | wood | concrete | other ]`, representing the final known surface on which the bottom layer of hay bales was stored.

<details>
  <summary>More about <code>final_surface_type</code></summary>

  <p>Describes the surface on which the bottom layer of bales was stored during the final storage stage.</p>
</details>

### `final_airflow_condition`
- **Data type**: `enum`  
- **Valid values**: An enumerated value: `[ natural ventilation | forced ventilation | enclosed with limited airflow | unknown ]`, representing the final known airflow characteristics of the hay storage environment.

<details>
  <summary>More about <code>final_airflow_condition</code></summary>

  <p>Describes the airflow conditions in the final storage environment. Adequate airflow reduces spoilage risk.</p>
</details>

### `restacked_since_baling`
- **Data type**: `enum`  
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether the hay was restacked at any point after baling and prior to sale or transfer.

<details>
  <summary>More about <code>restacked_since_baling</code></summary>

  <p>Indicates whether the hay was restacked or relocated at any point after its original baling. Restacking may lead to leaf loss and nutrient degradation.</p>
</details>

### `visible_moisture_damage`
- **Data type**: `enum`  
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether visible moisture damage was observed during the final stage of storage prior to sale or transfer.

<details>
  <summary>More about <code>visible_moisture_damage</code></summary>

  <p>Indicates whether there are visible signs of moisture damage on any portion of the hay, such as mold, discoloration, or odor.</p>
</details>

### `handling_events`
- **Data type**: `object[]`  
- **Structure**: A sequential list of storage and handling events from baling to sale. Each event may include the following fields:

  - `location_type` (`string`) – e.g., `farm`, `dealer yard`, `export staging`
  - `storage_structure` (`string`) – e.g., `enclosed barn`, `tarp-covered`
  - `surface_type` (`string`) – e.g., `pallets`, `ground`, `concrete`
  - `airflow_condition` (`string`) – e.g., `natural ventilation`, `limited airflow`
  - `duration_estimate` (`string`) – e.g., `"10–15 days"`, `"~1 month"`
  - `restacked` (`boolean`) – Whether the hay was restacked at this stage

??? example "Example block"
    ```yaml
    handling_events:
      - location_type: farm
        storage_structure: enclosed barn
        surface_type: pallets
        airflow_condition: natural ventilation
        duration_estimate: "30 days"
        restacked: false

      - location_type: broker yard
        storage_structure: tarp-covered
        surface_type: ground
        airflow_condition: enclosed with limited airflow
        duration_estimate: "10–15 days"
        restacked: true
    ```

## Nutrient analysis

### Sample processing

#### `hay_tested`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, representing whether a forage analysis has been conducted on the hay.

<details>
  <summary>More about <code>hay_tested</code></summary>

  <p>This field indicates whether a forage analysis has been performed on this hay. A value of <code>true</code> signifies that the hay has been tested through a lab or analytical facility. A value of <code>false</code> indicates that no testing has been done, while <code>unknown</code> allows for the possibility that the seller is unsure whether testing has occurred—e.g., in the case of a broker or distributor.</p>

</details>

#### `hay_sample_date`
- **Data type**: `datetime`
- **Valid values**: A date in `YYYYMMDD` format representing the date on which the hay sample was collected for analysis.

<details>
  <summary>More about <code>hay_sample_date</code></summary>

  <p>This field records the date on which the hay sample was collected for laboratory analysis. Accurate sample dating is important for interpreting results in the context of hay storage time, nutrient degradation, and marketing timelines.</p>

  <p>Sampling should reflect the hay offered for sale and should be conducted using representative methods, such as a coring probe across multiple bales. Some laboratories require the sample date for regulatory or archival purposes.</p>

</details>

#### `hay_sampler_independent`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, indicating whether the hay sample was collected by an independent third party.

<details>
  <summary>More about <code>hay_sampler_independent</code></summary>

  <p>This field indicates whether the individual or entity that collected the hay sample was independent of the seller. A value of <code>true</code> denotes that the sample was taken by a third party, such as a certified lab technician or agricultural extension agent, with no financial interest in the sale of the hay.</p>

  <p>A value of <code>false</code> indicates the sample was collected by the seller or someone affiliated with the seller. A value of <code>unknown</code> applies when the identity or affiliation of the sampler is not known.</p>

  <p>This distinction may influence the buyer’s confidence in the validity and impartiality of the analysis results, particularly in high-value transactions or formal feed programs.</p>

</details>

#### `hay_sampler_certified`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ true | false | unknown ]`, indicating whether the hay sample was collected by a certified forage or feed sampler.

<details>
  <summary>More about <code>hay_sampler_certified</code></summary>

  <p>This field indicates whether the person who collected the hay sample holds a recognized certification in forage or feed sampling. A value of <code>true</code> means the sampler was certified by a qualified authority—such as a state agriculture department, accredited laboratory, or national hay testing council—at the time the sample was collected.</p>

  <p>A value of <code>false</code> denotes that the sampler was not certified, while <code>unknown</code> applies when certification status is not known or not disclosed.</p>

  <p>Certified sampling can improve the credibility and repeatability of forage analysis, especially in cases where sampling technique significantly influences test results.</p>

</details>

#### `hay_sampling_protocol`
- **Data type**: `enum`
- **Valid values**: **Valid values**: An enumerated value: `[ NFTA | other ]`, indicating the protocol followed during hay sample collection.

<details>
  <summary>More about <code>hay_sampling_protocol</code></summary>

  <p>This field identifies the protocol used for collecting the hay sample. A value of <code>NFTA</code> indicates the sample was collected according to guidelines established by the National Forage Testing Association (NFTA), which include specifications for core sampling depth, number of cores per lot, sampling equipment, and bale selection.</p>

  <p>A value of <code>other</code> signifies that a different protocol was used—such as a custom, lab-specific, or industry-standard method outside NFTA guidelines. Users may wish to capture additional descriptive detail in a separate comments field if <code>other</code> is selected.</p>

  <p>The sampling protocol can affect the reliability and comparability of analytical results and may be a key consideration in quality assurance or product claims.</p>

</details>

#### `hay_testing_laboratory`
- **Data type**: `enum`
- **Valid values**: An enumerated value corresponding to a specific laboratory from an open, freely-available database maintained by Lode or another organization or, if self-tested, <code>Internal lab</code>.

<details>
  <summary>More about <code>hay_testing_laboratory</code></summary>

  <p>This field identifies the laboratory responsible for conducting the forage analysis. Accurate and transparent reporting of the testing laboratory helps ensure confidence in test results, supports traceability, and enables standardized reporting across producers and regions.</p>

  <p>For external labs, the enumerated list should include commonly used, certified forage testing labs—many of which participate in the National Forage Testing Association (NFTA) proficiency program or equivalent international standards.</p>

  <p>If analysis was conducted using in-house resources, enter <code>Internal lab</code>. It is advisable for sellers selecting this value to provide documentation of their testing procedures and equipment calibration where appropriate.</p>

</details>

#### `hay_testing_method`
- **Data type**: `enum`
- **Valid values**: An enumerated value: `[ Chemical analysis | Near Infrared Reflectance (NIR) spectroscopy | Both chemical analysis and NIR ]`, indicating the laboratory method used to analyze the hay sample.

<details>
  <summary>More about <code>hay_testing_method</code></summary>

  <p>This field identifies the analytical method used to evaluate the hay sample. It provides context for interpreting the precision and reliability of reported forage values.</p>

  <ul>
    <li><code>Chemical analysis</code>: Refers to traditional wet chemistry methods. These are highly accurate and are the benchmark for calibrating other methods but tend to be more time-consuming and costly.</li>
    <li><code>Near Infrared Reflectance (NIR) spectroscopy</code>: A rapid, cost-effective, and commonly used method. Results are based on comparison to a database of chemically analyzed samples and can vary in accuracy depending on sample type and calibration quality.</li>
    <li><code>Both chemical analysis and NIR</code>: Indicates that both methods were used on the same sample, typically to validate results or to supplement data with additional metrics only available via one of the two methods.</li>
  </ul>

  <p>Understanding the method used is essential for evaluating comparability across samples and for determining suitability for ration formulation or regulatory use.</p>

</details>

#### `hay_testing_date`
- **Data type**: `datetime`
- **Valid values**: A date in YYYYMMDD format representing the testing date for this hay.

<details>
  <summary>More about <code>hay_testing_date</code></summary>

  <p>This field records the date on which the laboratory analysis of the hay sample was completed. It helps establish the timeline between harvest, sampling, and testing, which may influence the interpretation of results—especially for parameters affected by storage conditions or time delays (e.g., mold development or nutrient degradation).</p>

  <p>Use the format <code>YYYYMMDD</code> to ensure consistency. If the exact testing date is not known but the year is, implementers may use the convention of double zeroes for unknown month or day (e.g., <code>20240000</code> or <code>20240500</code>).</p>

</details>

### Suggestions to Consider (Cross-field Validation and Extensions)

These enhancements are optional but may improve clarity, data consistency, and user experience in system implementations.

#### Conditional Field Visibility or Validation

- If `hay_tested = false`, then all remaining fields in the *Sample Processing* group may be hidden, disabled, or flagged as not applicable.
- If `hay_sampler_certified = true`, then `hay_sampler_independent` should not be `unknown` (implies there is known info about the sampler).
- If `hay_testing_method = both`, it is recommended that the lab selected in `hay_testing_laboratory` be capable of providing both services.

#### Additional Field (Optional)
- **`hay_testing_lab_other`** (optional free-text field)
  - **Purpose**: Captures lab name if `hay_testing_laboratory = other`.
  - **Use case**: Supports small or international labs not yet registered in a master lab list.

#### Date Consistency Check
- Ensure that `hay_testing_date` is not earlier than `hay_sample_date`.
  - Helps maintain chronological integrity of sample collection and analysis.

#### Optional Implementation Note
- Systems may optionally display warnings or soft alerts (not hard errors) when field combinations are logically inconsistent.

### Base values

#### `moisture_content`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the moisture content of the hay sample, expressed as a percentage of total weight. This value typically ranges from `5.0%` to `20.0%` in properly cured hay and is the complement of dry matter.

<details>
  <summary>More about <code>moisture_content</code></summary>

  <p>Moisture content is the percentage of the sample's total weight that consists of water. It is the inverse of dry matter and plays a critical role in hay storage, preservation, and nutritional calculations.</p>

  <p>Properly cured hay typically contains between <code>8%</code> and <code>15%</code> moisture. Values above <code>20%</code> may increase the risk of spoilage, mold, or spontaneous combustion during storage. Moisture content is used to convert lab values to either an "as-fed" or "dry matter" basis.</p>

  <p>Forage testing labs may measure moisture directly or derive it by subtracting dry matter from 100%.</p>

</details>

#### `dry_matter`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the dry matter content of the hay sample, expressed as a percentage of total weight. This value is the complement of moisture content and typically ranges from `80.0%` to `95.0%` in properly cured hay.

<details>
  <summary>More about <code>dry_matter</code></summary>

  <p>Dry matter is the portion of the forage that remains after all moisture has been removed. It includes all nutrients — such as fiber, protein, minerals, and energy — and is the standard basis for comparing feeds and formulating rations.</p>

  <p>This value is the mathematical complement of moisture content; that is, <code>dry matter = 100 - moisture content</code>. Most properly stored hay will contain <code>85% to 92%</code> dry matter. Lower values may indicate elevated moisture and a risk of spoilage or heating during storage.</p>

  <p>All nutrient values are typically reported on a dry matter basis to eliminate dilution effects from water and ensure comparability across feed types.</p>

</details>

### Index values

#### `relative_feed_value`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the Relative Feed Value (RFV) of the hay sample. Typical values range from `80` to `200`, with higher values indicating better digestibility and intake potential.

<details>
  <summary>More about <code>relative_feed_value</code></summary>

  <p>Relative Feed Value (RFV) is a standardized index used to estimate the overall quality of hay and other forages based on two key factors: <strong>digestibility</strong> and <strong>potential intake</strong>. It is calculated from Acid Detergent Fiber (ADF) and Neutral Detergent Fiber (NDF) values using the following formula:</p>

  <pre>RFV = (Dry Matter Intake %) × (Digestible Dry Matter %) ÷ 1.29</pre>

  <p>RFV is scaled such that full-bloom alfalfa has an index of 100. Higher values suggest improved animal performance due to increased nutrient availability and voluntary intake. For example:</p>

  <ul>
    <li><code>> 170</code>: Prime (top-grade dairy hay)</li>
    <li><code>150–170</code>: Premium</li>
    <li><code>125–149</code>: Good</li>
    <li><code>100–124</code>: Fair</li>
    <li><code>< 100</code>: Poor or mature forage</li>
  </ul>

  <p>RFV does not account for crude protein or mineral content, and it is gradually being replaced in some systems by <strong>Relative Forage Quality (RFQ)</strong>, which incorporates fiber digestibility.</p>

</details>

#### `relative_forage_quality`

- **Data type**: `float`
- **Valid values**: A positive decimal value representing the Relative Forage Quality (RFQ) of the hay sample. Typical values range from `80` to `200+`, with higher values indicating greater digestibility and intake potential.

<details>
  <summary>More about <code>relative_forage_quality</code></summary>

  <p>Relative Forage Quality (RFQ) is an enhanced forage index that estimates overall feed value by incorporating both potential intake and fiber digestibility. It improves upon Relative Feed Value (RFV) by replacing Acid Detergent Fiber (ADF) with Total Digestible Nutrients (TDN) and factoring in Neutral Detergent Fiber Digestibility (NDFD), when available.</p>

  <p>RFQ is calculated using formulas like:</p>

  <pre>RFQ = (DMI, % of BW) × (TDN, % of DM) ÷ 1.23</pre>

  <p>where:</p>
  
  <ul>
    <li>DMI = Dry Matter Intake, based on NDF</li>
    <li>TDN = Total Digestible Nutrients, based on ADF and NDFD</li>
  </ul>

  <p>RFQ better reflects the true feeding value of forage for ruminants than RFV, especially for grasses, mixed forages, and those with high fiber digestibility.</p>

  <p>Like RFV, RFQ is scaled such that full-bloom alfalfa has a value of 100. For example:</p>

  <ul>
    <li><code>> 170</code>: Prime</li>
    <li><code>150–170</code>: Premium</li>
    <li><code>130–149</code>: Good</li>
    <li><code>100–129</code>: Fair</li>
    <li><code>< 100</code>: Low quality</li>
  </ul>

  <p>RFQ is now the preferred index in many extension and laboratory reports, particularly where NDFD is measured or predicted.</p>

</details>

### NRC 2001 energy

#### `digestible_energy_1x_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the digestible energy (DE) of the hay sample in megacalories per pound (Mcal/lb), calculated at maintenance-level intake (1X). Typical values range from `0.85` to `1.25 Mcal/lb`.

<details>
  <summary>More about <code>digestible_energy_1x_mcal_per_lb</code></summary>

  <p>Digestible Energy (DE) is an intermediate measure of forage energy content, calculated as the gross energy of the feed minus fecal energy losses. It is a precursor to metabolizable and net energy calculations.</p>

  <p>This value is expressed in megacalories per pound of feed on a dry matter basis. The <code>1X</code> designation refers to maintenance-level intake, which avoids energy-use adjustments for production (e.g., lactation or growth).</p>

  <p>Typical DE values for hay range from <code>0.85</code> to <code>1.25 Mcal/lb</code>, with higher values indicating better digestibility and energy availability. This field is used in ration formulation, particularly for horses, beef cattle, and sheep.</p>

</details>

#### `metabolizable_energy_1x_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the metabolizable energy (ME) of the hay sample in megacalories per pound (Mcal/lb), calculated at maintenance-level intake (1X). Typical values range from `0.75` to `1.10 Mcal/lb`.

<details>
  <summary>More about <code>metabolizable_energy_1x_mcal_per_lb</code></summary>

  <p>Metabolizable Energy (ME) is calculated as the Digestible Energy (DE) of the forage minus energy lost as gases (primarily methane) and in urine. It represents the portion of energy available for maintenance and production in the animal.</p>

  <p>The <code>1X</code> label refers to a baseline intake level (maintenance), meaning this energy value does not include intake adjustments for increased metabolic demand such as lactation or growth.</p>

  <p>Typical forage ME values range from <code>0.75</code> to <code>1.10 Mcal/lb</code> on a dry matter basis. This field is commonly used in ration formulation for ruminants and equines and serves as the foundation for calculating net energy values.</p>

</details>

#### `net_energy_lactation_3x_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy of lactation (NEL) of the hay sample in megacalories per pound (Mcal/lb), adjusted for intake at three times maintenance level (3X). Typical values range from `0.60` to `0.80 Mcal/lb`.

<details>
  <summary>More about <code>net_energy_lactation_3x_mcal_per_lb</code></summary>

  <p>Net Energy of Lactation (NEL) estimates the energy available from forage for milk production after accounting for all energy losses — including fecal, urinary, gaseous, and heat increment. It is a critical measure in dairy cow rations.</p>

  <p>The <code>3X</code> designation reflects a standardized dry matter intake level that corresponds to three times the maintenance energy requirement. This intake level reflects typical consumption for lactating cows and improves comparability of NEL values across forages.</p>

  <p>Values typically range from <code>0.60</code> to <code>0.80 Mcal/lb</code> on a dry matter basis. This value is used extensively in balancing dairy rations and estimating milk yield potential.</p>

</details>

#### `net_energy_maintenance_3x_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy available for maintenance (NEM) of the hay sample in megacalories per pound (Mcal/lb), assuming dry matter intake at three times maintenance level (3X). Typical values range from `0.50` to `0.75 Mcal/lb`.

<details>
  <summary>More about <code>net_energy_maintenance_3x_mcal_per_lb</code></summary>

  <p>Net Energy for Maintenance (NEM) is the portion of forage energy available to support the basic metabolic functions of livestock — such as body temperature regulation, organ function, and standing activity — without contributing to growth or production.</p>

  <p>This value is calculated after subtracting all forms of energy loss, including fecal, urinary, gaseous, and heat increment losses. The <code>3X</code> designation reflects intake level three times above basal maintenance, which aligns with standardized assumptions used in NRC 2001 energy modeling.</p>

  <p>Typical hay samples range from <code>0.50</code> to <code>0.75 Mcal/lb</code> NEM on a dry matter basis. Higher values indicate better-quality forage for maintaining body weight without needing energy supplementation.</p>

</details>

#### `net_energy_gain_3x_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy for gain (NEG) of the hay sample in megacalories per pound (Mcal/lb), assuming dry matter intake at three times maintenance level (3X). Typical values range from `0.25` to `0.60 Mcal/lb`.

<details>
  <summary>More about <code>net_energy_gain_3x_mcal_per_lb</code></summary>

  <p>Net Energy for Gain (NEG) estimates the energy available for body weight gain — such as muscle and fat deposition — after an animal’s maintenance requirements are met. It is particularly important for growing and finishing beef cattle and feedlot operations.</p>

  <p>This value is expressed in megacalories per pound (Mcal/lb) of dry matter, with the <code>3X</code> intake assumption standardizing the calculation across feeding models.</p>

  <p>Higher NEG values are associated with higher-quality forages and support faster average daily gains (ADG). Typical hay samples fall between <code>0.25</code> and <code>0.60 Mcal/lb</code>.</p>

</details>

#### `digestible_energy_1x_mcal_per_kg`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the digestible energy (DE) of the hay sample in megacalories per kilogram (Mcal/kg), calculated at maintenance-level intake (1X). Typical values range from `1.8` to `2.6 Mcal/kg`.

<details>
  <summary>More about <code>digestible_energy_1x_mcal_per_kg</code></summary>

  <p>Digestible Energy (DE) measures the amount of energy in forage that is available to livestock after subtracting fecal losses from the gross energy content. This value is expressed here in <code>Mcal/kg</code> to support international and metric-based ration formulations.</p>

  <p>The <code>1X</code> designation indicates that the estimate is based on intake equivalent to one times maintenance energy requirement — a standard NRC basis. Typical DE values for hay range from <code>1.8</code> to <code>2.6 Mcal/kg</code> on a dry matter basis.</p>

  <p>While U.S. feeding systems often use <code>Mcal/lb</code>, metric values are common in international livestock nutrition contexts.</p>

</details>

#### `metabolizable_energy_1x_mcal_per_kg`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the metabolizable energy (ME) of the hay sample in megacalories per kilogram (Mcal/kg), calculated at maintenance-level intake (1X). Typical values range from `1.6` to `2.3 Mcal/kg`.

<details>
  <summary>More about <code>metabolizable_energy_1x_mcal_per_kg</code></summary>

  <p>Metabolizable Energy (ME) is the amount of energy available to the animal after subtracting fecal, urinary, and gaseous losses from the Digestible Energy (DE) of the forage. This value is expressed in <code>Mcal/kg</code> to support metric feeding systems.</p>

  <p>The <code>1X</code> label signifies that the value is based on a dry matter intake equal to maintenance-level energy requirements. This is a standard assumption in NRC 2001 energy models for ruminants.</p>

  <p>Most hays provide between <code>1.6</code> and <code>2.3 Mcal/kg</code> of metabolizable energy on a dry matter basis. This value is essential for ration formulation, especially when comparing forage sources in metric-based nutrition models.</p>

</details>

#### `net_energy_lactation_3x_mcal_per_kg`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy of lactation (NEL) of the hay sample in megacalories per kilogram (Mcal/kg), assuming dry matter intake at three times maintenance level (3X). Typical values range from `1.3` to `1.8 Mcal/kg`.

<details>
  <summary>More about <code>net_energy_lactation_3x_mcal_per_kg</code></summary>

  <p>Net Energy for Lactation (NEL) represents the energy available from forage for milk production, after all losses from feces, urine, gas, and heat increment have been subtracted. This field expresses that value in <code>Mcal/kg</code> to support metric-based feed systems.</p>

  <p>The <code>3X</code> label reflects a standardized dry matter intake level equivalent to three times maintenance, in line with NRC 2001 energy modeling conventions. This assumption supports comparability of values across different forages and feeding scenarios.</p>

  <p>Most hays fall between <code>1.3</code> and <code>1.8 Mcal/kg</code> NEL on a dry matter basis. Higher values indicate improved energy density and are associated with earlier-cut or legume-rich forages suitable for lactating animals.</p>

</details>

#### `net_energy_maintenance_3x_mcal_per_kg`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy for maintenance (NEM) of the hay sample in megacalories per kilogram (Mcal/kg), assuming dry matter intake at three times maintenance level (3X). Typical values range from `1.1` to `1.6 Mcal/kg`.

<details>
  <summary>More about <code>net_energy_maintenance_3x_mcal_per_kg</code></summary>

  <p>Net Energy for Maintenance (NEM) is the portion of forage energy available to maintain essential animal functions such as thermoregulation, circulation, and tissue maintenance. It is a core energy metric in both beef and dairy nutrition models.</p>

  <p>The <code>3X</code> designation reflects dry matter intake at three times the maintenance requirement, following the standard intake assumption of the NRC 2001 model. This value is expressed in <code>Mcal/kg</code> to support international and metric-based nutrition systems.</p>

  <p>Forage samples typically range from <code>1.1</code> to <code>1.6 Mcal/kg</code> of NEM. Higher values indicate better energy efficiency for livestock maintenance needs, with legume and early-cut forages tending to score higher.</p>

</details>

#### `net_energy_gain_3x_mcal_per_kg`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the net energy for gain (NEG) of the hay sample in megacalories per kilogram (Mcal/kg), assuming dry matter intake at three times maintenance level (3X). Typical values range from `0.55` to `1.3 Mcal/kg`.

<details>
  <summary>More about <code>net_energy_gain_3x_mcal_per_kg</code></summary>

  <p>Net Energy for Gain (NEG) estimates the amount of energy available in forage for supporting body weight gain — including muscle and fat deposition — after an animal’s maintenance needs are met.</p>

  <p>This value is reported in <code>Mcal/kg</code> on a dry matter basis, aligning with metric-based nutrition systems. The <code>3X</code> intake label conforms to NRC 2001 energy modeling, assuming animals are consuming dry matter at three times their maintenance requirement.</p>

  <p>Most forages range between <code>0.55</code> and <code>1.3 Mcal/kg</code> NEG. Higher values correspond to higher energy-density hays and support greater average daily gains (ADG), especially in growing and finishing cattle.</p>

</details>

#### `tdn_1x`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the Total Digestible Nutrients (TDN) of the hay sample, expressed as a percentage of dry matter, at maintenance-level intake (1X). Typical values range from `50.0%` to `70.0%`.

<details>
  <summary>More about <code>tdn_1x</code></summary>

  <p>Total Digestible Nutrients (TDN) is an estimate of the total amount of digestible fiber, protein, lipid, and carbohydrate in a forage. It serves as a key indicator of the forage’s overall energy content.</p>

  <p>The <code>1X</code> designation indicates that the TDN value is calculated at an intake level equal to one times the animal’s maintenance requirement. This is standard for NRC 2001 models and serves as the baseline for comparing forages.</p>

  <p>TDN is expressed as a percentage of dry matter. Most hays range from <code>50%</code> (low-quality grass) to <code>70%</code> (high-quality legume). Higher TDN values indicate greater energy availability and generally correlate with earlier harvest maturity and better digestibility.</p>

</details>

### Protein and protein fractions

#### `crude_protein`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the crude protein (CP) content of the hay sample, expressed as a percentage of dry matter. Typical values range from `6.0%` to `25.0%`.

<details>
  <summary>More about <code>crude_protein</code></summary>

  <p>Crude Protein (CP) is an estimate of the total protein content in forage, calculated by measuring the nitrogen content and multiplying by a factor of 6.25. This includes both true protein and non-protein nitrogen (NPN) compounds.</p>

  <p>Crude protein is expressed on a dry matter basis to eliminate dilution by moisture. Most grass hays contain <code>6%–12%</code> CP, while legume hays (such as alfalfa) may contain <code>15%–25%</code> CP, depending on maturity and harvest conditions.</p>

  <p>CP is a standard input for animal ration formulation and is used to evaluate whether a forage meets the protein requirements of different livestock classes.</p>

</details>

#### `available_protein`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the available protein content of the hay sample, expressed as a percentage of dry matter. Typical values range from `5.0%` to `22.0%`.

<details>
  <summary>More about <code>available_protein</code></summary>

  <p>Available protein is the portion of crude protein (CP) that remains digestible and usable by the animal after accounting for reductions due to heat damage, insolubility, and fiber-bound nitrogen. It reflects the true nutritional value of the protein in the forage.</p>

  <p>This value is often calculated as:</p>

  <pre>Available Protein = Crude Protein − Acid Detergent Insoluble Crude Protein (ADF-CP)</pre>

  <p>Available protein is particularly important when evaluating hays that have been exposed to moisture during harvest or that may have undergone Maillard reactions (browning) due to overheating in storage.</p>

  <p>Values are expressed on a dry matter basis. Legumes tend to have higher available protein content than grasses, and well-preserved hay will typically retain most of its crude protein as available protein.</p>

</details>

#### `acid_detergent_insoluble_crude_protein`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the acid detergent insoluble crude protein (ADF-CP) content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.3%` to `5.0%`.

<details>
  <summary>More about <code>acid_detergent_insoluble_crude_protein</code></summary>

  <p>Acid Detergent Insoluble Crude Protein (ADF-CP) is the fraction of crude protein that is bound to indigestible fiber components in the forage and is considered largely unavailable to ruminants. This includes protein that has been rendered inaccessible due to heat damage during harvest or storage.</p>

  <p>ADF-CP is a key factor in calculating <code>available_protein</code>:</p>

  <pre>Available Protein = Crude Protein − ADF-CP</pre>

  <p>Higher ADF-CP values typically indicate poorer forage quality. Values above <code>3.0%</code> suggest significant heat damage or poor harvest conditions, and forages with high ADF-CP may underperform despite high crude protein content.</p>

</details>

#### `adjusted_crude_protein`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the adjusted crude protein (ACP) content of the hay sample, expressed as a percentage of dry matter. Typical values range from `5.0%` to `22.0%`.

<details>
  <summary>More about <code>adjusted_crude_protein</code></summary>

  <p>Adjusted Crude Protein (ACP) represents the total protein content of the forage after correcting for indigestible fractions, such as heat-damaged or fiber-bound protein. It provides a more realistic estimate of protein availability for livestock.</p>

  <p>ACP is typically calculated as:</p>

  <pre>Adjusted Crude Protein = Crude Protein − ADF-CP (or other unavailable protein fractions)</pre>

  <p>This field may overlap conceptually with <code>available_protein</code>, depending on how the lab or model calculates each. In your data model, this field can be retained to preserve compatibility with test results from labs that report both.</p>

  <p>Values are expressed on a dry matter basis. Accurate representation of ACP is critical in formulating protein-sufficient diets, especially when working with weather-damaged hay.</p>

</details>

#### `soluble_protein_%_cp`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the soluble protein fraction of the hay sample, expressed as a percentage of crude protein (% of CP). Typical values range from `15.0%` to `40.0%`.

<details>
  <summary>More about <code>soluble_protein_%_cp</code></summary>

  <p>Soluble Protein is the portion of crude protein (CP) that dissolves rapidly in rumen fluid and is quickly available for microbial fermentation. It includes non-protein nitrogen (NPN), peptides, amino acids, and some true protein.</p>

  <p>This value is expressed as a percentage of the forage’s total crude protein. A typical range for hay is <code>15%–40%</code> of CP, with higher values indicating faster ruminal degradation and potentially greater risk of nitrogen imbalance if not matched with available energy.</p>

  <p>Soluble protein is a component of <code>degradable protein</code> and is often used in formulating balanced rations for optimal microbial protein synthesis.</p>

</details>

#### `degradable_protein_%_cp`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the degradable crude protein content of the hay sample, expressed as a percentage of crude protein (% of CP). Typical values range from `30.0%` to `80.0%`.

<details>
  <summary>More about <code>degradable_protein_%_cp</code></summary>

  <p>Degradable Protein (also known as Ruminally Degradable Protein or RDP) refers to the fraction of crude protein that is broken down by rumen microbes into ammonia, peptides, and amino acids. This component supports microbial protein synthesis and overall fermentation efficiency.</p>

  <p>This value is expressed as a percentage of the forage’s total crude protein. It includes <code>soluble protein</code> as a subset, along with slowly degradable true protein fractions.</p>

  <p>Values typically range from <code>30%–80%</code> of CP. Forages with excessive degradability may require supplementation with rumen undegradable protein (RUP) to balance nitrogen supply with energy availability.</p>

</details>

#### `neutral_detergent_insoluble_crude_protein`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the neutral detergent insoluble crude protein (NDICP) content of the hay sample, expressed as a percentage of dry matter. Typical values range from `1.0%` to `6.0%`.

<details>
  <summary>More about <code>neutral_detergent_insoluble_crude_protein</code></summary>

  <p>Neutral Detergent Insoluble Crude Protein (NDICP) refers to the fraction of forage protein that is insoluble in the neutral detergent solution used to measure fiber (NDF). It is associated with the cell wall and may be partially or fully indigestible depending on forage quality and animal passage rate.</p>

  <p>NDICP is typically larger than ADF-CP, as it includes both indigestible and potentially digestible fiber-bound protein. It plays a role in estimating the <code>rumen undegradable protein</code> (RUP) and <code>metabolizable protein</code> supply.</p>

  <p>Values are expressed on a dry matter basis. High NDICP may indicate fiber maturity, weather damage, or overmature forage.</p>

</details>

### Amino acids

#### `lysine`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the lysine content of the forage sample, expressed as a percentage of dry matter. Values typically range between `0.1` and `3.0`.

<details>
  <summary>More about <code>lysine</code></summary>

  <p>Lysine is an essential amino acid required for growth, milk production, and muscle development. This field reports the lysine content of the hay sample on a dry matter basis. Results are typically derived from laboratory analysis and may vary based on forage type and maturity.</p>

  <p>Values may be estimated via Near Infrared Reflectance (NIR) or measured via wet chemistry. For most hay samples, lysine content will fall within a typical range of `0.3%` to `1.5%` of dry matter.</p>

</details>

#### `methionine`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the methionine content of the forage sample, expressed as a percentage of dry matter. Values typically range between `0.1` and `0.5`.

<details>
  <summary>More about <code>methionine</code></summary>

  <p>Methionine is an essential amino acid involved in protein synthesis and methylation processes. It is particularly important for dairy animals and poultry. This field reports the methionine content of the hay sample on a dry matter basis, as determined by laboratory analysis.</p>

  <p>Values are commonly derived from Near Infrared Reflectance (NIR) estimates or direct wet chemistry testing. Typical methionine levels in legume or grass hay range from `0.1%` to `0.4%` of dry matter.</p>

</details>

### Carbohydrates

#### `acid_detergent_fiber`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the acid detergent fiber (ADF) content of the hay sample, expressed as a percentage of dry matter. Values typically range from `20.0` to `45.0`.

<details>
  <summary>More about <code>acid_detergent_fiber</code></summary>

  <p>Acid Detergent Fiber (ADF) represents the fraction of forage composed of cellulose and lignin — the least digestible plant components. It is an important indicator of forage quality and directly correlates with digestibility. As ADF increases, digestibility decreases.</p>

  <p>This value is expressed as a percentage of dry matter and is typically determined by laboratory analysis using either wet chemistry or NIR methods.</p>

</details>

#### `neutral_detergent_fiber`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the neutral detergent fiber (NDF) content of the hay sample, expressed as a percentage of dry matter. Values typically range from `30.0` to `70.0`.

<details>
  <summary>More about <code>neutral_detergent_fiber</code></summary>

  <p>Neutral Detergent Fiber (NDF) quantifies the total cell wall content of forage — including hemicellulose, cellulose, and lignin. It is a key determinant of forage bulk and limits dry matter intake, especially in ruminants.</p>

  <p>This field expresses NDF as a percentage of dry matter, and it is typically determined through laboratory analysis via NIR spectroscopy or wet chemistry. Lower NDF is generally associated with higher quality and palatability.</p>

</details>

#### `lignin`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the lignin content of the hay sample, expressed as a percentage of dry matter. Values typically range from `2.0` to `12.0`.

<details>
  <summary>More about <code>lignin</code></summary>

  <p>Lignin is a complex, indigestible polymer found in plant cell walls. Its concentration significantly influences forage digestibility. As lignin content increases, the digestibility of both cellulose and hemicellulose declines.</p>

  <p>This field expresses lignin as a percentage of dry matter. It is typically measured through laboratory analysis, with values varying depending on forage maturity, plant species, and environmental conditions.</p>

</details>

#### `non_fiber_carbohydrates`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the non-fiber carbohydrate (NFC) content of the hay sample, expressed as a percentage of dry matter. Values typically range from `20.0` to `45.0`.

<details>
  <summary>More about <code>non_fiber_carbohydrates</code></summary>

  <p>Non-Fiber Carbohydrates (NFC) represent the portion of forage that consists of sugars, starches, pectins, and organic acids. These components are highly digestible and contribute significantly to the energy value of the forage, particularly in ruminant diets.</p>

  <p>NFC is typically calculated using the formula:  
  <code>NFC = 100 - (NDF + CP + Fat + Ash)</code></p>

  <p>This value is expressed as a percentage of dry matter. Forages with high NFC values provide more rapidly fermentable carbohydrates, which can be beneficial or risky depending on the animal class and overall diet formulation.</p>

</details>

#### `starch`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the starch content of the hay sample, expressed as a percentage of dry matter. Values typically range from `0.0` to `40.0`, depending on forage type.

<details>
  <summary>More about <code>starch</code></summary>

  <p>Starch is a non-structural carbohydrate that contributes substantially to the energy density of a forage. It is highly fermentable in the rumen and often derived from grain content or immature plant material in mixed forages.</p>

  <p>This value is expressed as a percentage of dry matter and is determined through laboratory analysis, typically via wet chemistry or NIR. While starch content is usually low in grass and legume hays, it may be higher in small grain or mixed forages harvested at the boot or dough stage.</p>

</details>

#### `water_soluble_carbohydrates`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the water-soluble carbohydrate (WSC) content of the hay sample, expressed as a percentage of dry matter. Values typically range from `2.0` to `20.0`.

<details>
  <summary>More about <code>water_soluble_carbohydrates</code></summary>

  <p>Water Soluble Carbohydrates (WSC) include sugars and other carbohydrates that dissolve in water and are rapidly fermentable. These carbohydrates affect both the palatability of the forage and its fermentation characteristics when ensiled.</p>

  <p>WSC is expressed as a percentage of dry matter. It is an important metric for animals sensitive to carbohydrate load — such as horses at risk of laminitis. It also plays a role in forage selection for high-energy diets or fermentation profiles.</p>

  <p>Values are typically determined via laboratory analysis using wet chemistry methods.</p>

</details>

#### `ethanol_soluble_carbohydrates`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the ethanol-soluble carbohydrate (ESC) content of the hay sample, expressed as a percentage of dry matter. Values typically range from `1.0` to `12.0`.

<details>
  <summary>More about <code>ethanol_soluble_carbohydrates</code></summary>

  <p>Ethanol Soluble Carbohydrates (ESC) are a subset of water-soluble carbohydrates that dissolve in 80% ethanol. ESC primarily includes monosaccharides and some disaccharides and is considered a more specific measure of simple sugars in forage.</p>

  <p>ESC is important for formulating rations for animals with metabolic sensitivity, such as horses with insulin resistance or laminitis. This field reports ESC as a percentage of dry matter, typically determined by laboratory wet chemistry.</p>

  <p>ESC values are always less than or equal to Water Soluble Carbohydrates (WSC), since WSC includes additional soluble polysaccharides not extracted by ethanol.</p>

</details>

### Fat

#### `crude_fat`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the crude fat content of the hay sample, expressed as a percentage of dry matter. Values typically range from `1.0` to `5.0`, though higher values may occur in certain treated or ensiled forages.

<details>
  <summary>More about <code>crude_fat</code></summary>

  <p>Crude fat represents the ether-extractable portion of the forage sample, including lipids, fatty acids, waxes, and other ether-soluble compounds. While forage is not typically high in fat, this metric contributes to overall energy calculations.</p>

  <p>Crude fat is expressed as a percentage of dry matter and is typically determined through laboratory extraction methods. Higher crude fat values may indicate the presence of oilseed additives or ensiled materials with higher lipid content.</p>

</details>

#### `total_fatty_acids`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the total fatty acid content of the hay sample, expressed as a percentage of dry matter. Values typically range from `0.8` to `3.5`.

<details>
  <summary>More about <code>total_fatty_acids</code></summary>

  <p>Total Fatty Acids (TFA) represent the portion of ether-extractable material in forage that consists specifically of true fatty acids. This field excludes waxes, pigments, and other non-nutritive ether solubles included in crude fat.</p>

  <p>TFA is a more precise indicator of a forage's energy potential and is commonly used in dairy ration models to estimate Net Energy of Lactation (NEL), Maintenance (NEM), and Gain (NEG).</p>

  <p>This value is expressed as a percentage of dry matter and is typically estimated using chemical extraction techniques or derived from crude fat values using a standard coefficient (e.g., 0.8 × crude fat).</p>

</details>

#### `rumen_unsaturated_fatty_acid_load`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the rumen unsaturated fatty acid load (RUFAL) of the hay sample, expressed in grams per kilogram of forage dry matter. Values for hay typically range from `2.0` to `10.0`, though higher values may be seen in oil-rich or ensiled forages.

<details>
  <summary>More about <code>rumen_unsaturated_fatty_acid_load</code></summary>

  <p>Rumen Unsaturated Fatty Acid Load (RUFAL) is a calculated value representing the concentration of unsaturated fatty acids that can impact rumen fermentation. High RUFAL levels are associated with an increased risk of milk fat depression (MFD) in dairy cattle due to altered rumen biohydrogenation pathways.</p>

  <p>This value is expressed in grams per kilogram of dry matter and is typically calculated from detailed fatty acid profiles. While forages generally have lower RUFAL values compared to byproduct feeds or oilseeds, some high-fat or ensiled hays may exceed typical levels.</p>

  <p>Monitoring RUFAL is essential in balanced ration formulation for lactating cows, especially when multiple feed components contribute to total dietary fat.</p>

</details>

### Energy and digestibility

#### Digestibility Metrics

##### `in_vitro_true_digestibility_30hr_percent_dm`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the in vitro true digestibility of the hay sample after 30 hours of fermentation, expressed as a percentage of dry matter. Values typically range from `50.0` to `90.0`.

<details>
  <summary>More about <code>in_vitro_true_digestibility_30hr_percent_dm</code></summary>

  <p>This field represents In Vitro True Digestibility (IVTD) at 30 hours, expressed as a percentage of dry matter. It reflects the proportion of the forage that is truly digestible by ruminants, based on simulated fermentation in a laboratory setting.</p>

  <p>Higher values indicate better forage quality and higher energy availability. IVTD is typically determined using rumen fluid or enzymatic simulations and is often used as a benchmark for comparing the feeding value of different hay types.</p>

  <p>This metric is particularly important for dairy and beef producers seeking to optimize forage efficiency and milk/meat production per unit of feed intake.</p>

</details>

##### `neutral_detergent_fiber_digestibility_30hr_percent_ndf`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the 30-hour in vitro digestibility of the neutral detergent fiber (NDF) portion of the hay sample, expressed as a percentage of NDF. Values typically range from `30.0` to `70.0`.

<details>
  <summary>More about <code>neutral_detergent_fiber_digestibility_30hr_percent_ndf</code></summary>

  <p>This field measures Neutral Detergent Fiber Digestibility (NDFD) after 30 hours of fermentation, expressed as a percentage of the total NDF content in the forage sample. It indicates how much of the fiber fraction can be digested by ruminants within a biologically relevant timeframe.</p>

  <p>Higher values correspond to more digestible fiber and are associated with improved feed efficiency and animal performance. This value is especially important in dairy nutrition models such as those used by the NRC and CNCPS.</p>

  <p>NDFD30 is typically measured through laboratory simulation using rumen fluid or enzymatic methods.</p>

</details>

##### `kd_percent_per_hr`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the rate of digestion (kd) of the forage sample, expressed in percent per hour. Values typically range from `2.0` to `8.0`.

<details>
  <summary>More about <code>kd_percent_per_hr</code></summary>

  <p>The `kd` value represents the fractional rate at which forage dry matter or fiber is digested in the rumen. It is expressed as a percentage of the component digested per hour (`%/hr`). This parameter is used in dynamic ruminant models to estimate forage retention time and nutrient availability.</p>

  <p>Higher `kd` values reflect faster digestion, typically associated with younger, more digestible forages. Lower values may indicate mature, weathered, or highly lignified material. Most `kd` values for NDF digestion fall between `2.0` and `8.0 %/hr`.</p>

  <p>Measured values are usually determined in vitro via rumen fluid incubation, or estimated via NIR calibration curves.</p>

</details>

##### `total_digestible_nutrients`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the total digestible nutrients (TDN) of the hay sample, expressed as a percentage of dry matter. Values typically range from `45.0` to `75.0`.

<details>
  <summary>More about <code>total_digestible_nutrients</code></summary>

  <p>Total Digestible Nutrients (TDN) is an aggregate energy metric that estimates the total amount of digestible material in a forage sample, expressed as a percentage of dry matter. TDN includes digestible fiber, crude protein, non-fiber carbohydrates, and fat (multiplied by 2.25).</p>

  <p>TDN is a standard value in forage analysis reports and is used extensively in ruminant nutrition modeling. Higher TDN values indicate higher energy content and generally higher forage quality. Values vary based on forage species, maturity, harvest conditions, and preservation method.</p>

  <p>TDN may be estimated from lab-measured nutrient fractions or predicted via Near Infrared Reflectance Spectroscopy (NIR).</p>

</details>

#### Species-Specific Energy Metrics

##### `horse_digestible_energy_mcal_per_lb`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the digestible energy (DE) of the hay sample for horses, expressed in megacalories per pound of dry matter. Values typically range from `0.80` to `1.20`.

<details>
  <summary>More about <code>horse_digestible_energy_mcal_per_lb</code></summary>

  <p>This field represents the Digestible Energy (DE) content of the hay sample for horses, expressed in megacalories per pound of dry matter. DE is the standard energy unit used in equine ration formulation and represents the amount of energy available to the horse after losses in feces are accounted for.</p>

  <p>Typical values vary by forage type and maturity. Grass hays generally range from `0.80` to `1.00 Mcal/lb`, while high-quality alfalfa can reach `1.15 Mcal/lb` or more. This field may be calculated from lab-measured nutrient fractions (e.g., TDN or NDF) or derived from empirical models for horse digestion.</p>

  <p>This value is useful for formulating diets based on energy requirements by class (maintenance, growth, lactation, work).</p>

</details>

### Minerals

#### `ash`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the ash content of the hay sample, expressed as a percentage of dry matter. Values typically range from `6.0` to `12.0`, with higher values indicating potential soil contamination.

<details>
  <summary>More about <code>ash</code></summary>

  <p>Ash is the total mineral residue remaining after complete combustion of a forage sample. It includes both essential macro- and microminerals, as well as any inorganic material introduced during harvest, such as dirt or sand.</p>

  <p>This field is expressed as a percentage of dry matter. Ash levels above `12–14%` are often considered abnormally high and may suggest soil contamination due to improper raking or baling from muddy fields.</p>

  <p>Ash values are important for both mineral balancing and energy calculations, as high ash reduces the organic matter portion of forage and thus its true energy density.</p>

</details>

#### `calcium`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the calcium content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.25` to `0.60` for grass hay and from `1.20` to `2.00` for legume hay.

<details>
  <summary>More about <code>calcium</code></summary>

  <p>Calcium (Ca) is an essential macromineral required for bone development, muscle contraction, nerve function, and milk production. Forage calcium content varies widely based on plant species, growth stage, and fertilization practices.</p>

  <p><strong>Grass hays</strong> — such as bermudagrass, timothy, or orchardgrass — typically contain between <code>0.25%</code> and <code>0.60%</code> calcium on a dry matter basis.</p>

  <p><strong>Legume hays</strong> — such as alfalfa or clover — generally contain much higher levels, ranging from <code>1.20%</code> to <code>2.00%</code> calcium on a dry matter basis.</p>

  <p>This value is typically determined through wet chemistry or NIR estimation. Accurate calcium values are essential in formulating balanced rations for dairy cattle, horses, goats, and other livestock, especially for preventing conditions such as hypocalcemia or milk fever.</p>

</details>

#### `phosphorus`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the phosphorus content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.15` to `0.35` for grass hay and from `0.25` to `0.45` for legume hay.

<details>
  <summary>More about <code>phosphorus</code></summary>

  <p>Phosphorus (P) is a macromineral that plays vital roles in skeletal health, energy metabolism, and reproductive function. It also supports microbial growth in the rumen, which is essential for digestion of fibrous feeds.</p>

  <p><strong>Grass hays</strong> generally contain between <code>0.15%</code> and <code>0.35%</code> phosphorus, depending on maturity, soil fertility, and harvest timing. <strong>Legume hays</strong> typically provide higher levels, ranging from <code>0.25%</code> to <code>0.45%</code>.</p>

  <p>Forage phosphorus deficiencies are common in certain regions and must be corrected through mineral supplementation. The calcium-to-phosphorus ratio is also an important consideration in ration formulation, especially for growing livestock and equine diets.</p>

</details>

#### `magnesium`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the magnesium content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.10` to `0.25` for grass hay and from `0.20` to `0.40` for legume hay.

<details>
  <summary>More about <code>magnesium</code></summary>

  <p>Magnesium (Mg) is an essential macromineral involved in neuromuscular function, energy metabolism, and bone formation. In ruminants, magnesium deficiencies can lead to grass tetany (hypomagnesemia), particularly in fast-growing spring grasses with high potassium levels.</p>

  <p><strong>Grass hays</strong> typically contain between <code>0.10%</code> and <code>0.25%</code> magnesium, while <strong>legume hays</strong> — such as alfalfa — generally contain <code>0.20%</code> to <code>0.40%</code>.</p>

  <p>This value is expressed as a percentage of dry matter and is usually measured by laboratory wet chemistry or estimated by NIR. Monitoring magnesium is important in mineral balancing, especially when potassium or nitrogen fertilization is high.</p>

</details>

#### `potassium`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the potassium content of the hay sample, expressed as a percentage of dry matter. Typical values range from `1.00` to `3.00` for grass hay and from `2.00` to `3.50` for legume hay.

<details>
  <summary>More about <code>potassium</code></summary>

  <p>Potassium (K) is an essential macromineral involved in fluid balance, muscle and nerve function, and plant health. While vital, excessive potassium in forage can impair absorption of magnesium and calcium in ruminants, contributing to conditions such as grass tetany and milk fever.</p>

  <p><strong>Grass hays</strong> generally contain between <code>1.00%</code> and <code>3.00%</code> potassium. <strong>Legume hays</strong> — especially when heavily fertilized — often range from <code>2.00%</code> to <code>3.50%</code>.</p>

  <p>Potassium levels above <code>3.00%</code> may require dietary adjustment or supplementation of other minerals to ensure metabolic balance, particularly in periparturient dairy cows or spring-calving beef herds.</p>

</details>

#### `sulfur`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the sulfur content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.10` to `0.25` for grass hay and from `0.20` to `0.35` for legume hay. Values above `0.40%` may pose a risk of toxicity.

<details>
  <summary>More about <code>sulfur</code></summary>

  <p>Sulfur (S) is an essential mineral used in the synthesis of sulfur-containing amino acids and the production of B-vitamins by rumen microbes. It supports structural tissue development, including wool, hair, and hooves.</p>

  <p><strong>Grass hays</strong> generally contain <code>0.10%</code> to <code>0.25%</code> sulfur, while <strong>legume hays</strong> may range from <code>0.20%</code> to <code>0.35%</code>. Excess sulfur — particularly when combined with high-sulfur water or distillers grains — can cause neurologic disorders such as polioencephalomalacia (PEM) in cattle and sheep.</p>

  <p>This value is expressed as a percentage of dry matter and is important when formulating rations for confined livestock, especially in high-performance beef and dairy systems.</p>

</details>

#### `chloride_ion`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the chloride ion (Cl⁻) content of the hay sample, expressed as a percentage of dry matter. Typical values range from `0.20` to `0.50`. Values above `0.60%` may indicate contamination or unusual environmental exposure.

<details>
  <summary>More about <code>chloride_ion</code></summary>

  <p>Chloride (Cl⁻) is a negatively charged electrolyte that contributes to acid-base balance, osmoregulation, and hydrochloric acid production in the digestive tract. In forage analysis, chloride is typically expressed as a percentage of dry matter.</p>

  <p>Chloride is particularly important in dairy nutrition for calculating the Dietary Cation-Anion Difference (DCAD), which influences calcium metabolism and the risk of milk fever. Forages with high chloride concentrations are often used in close-up rations to promote a mild metabolic acidosis.</p>

  <p>Most hays contain between <code>0.20%</code> and <code>0.50%</code> chloride. Concentrations above <code>0.60%</code> are uncommon and may result from exposure to salt-rich water, coastal spray, or chloride-containing fertilizers.</p>

</details>

#### `iron_ppm`
- **Data type**: `int`
- **Valid values**: A positive integer representing the iron content of the hay sample in parts per million (PPM). Typical values range from `100` to `500 PPM`; values above `1,000 PPM` may interfere with absorption of other trace minerals.

<details>
  <summary>More about <code>iron_ppm</code></summary>

  <p>Iron (Fe) is a trace mineral required for oxygen transport, enzyme systems, and immune function. It is generally abundant in forages and deficiency is rare. However, high iron levels — especially when combined with iron-rich water or supplements — can lead to reduced absorption of copper, zinc, and manganese.</p>

  <p>Forage iron is measured in parts per million (PPM) on a dry matter basis. Most hays contain between <code>100</code> and <code>500 PPM</code> iron. Levels above <code>1,000 PPM</code> may result from soil contamination or iron-rich irrigation water and may require attention to overall mineral balance.</p>

</details>

#### `zinc_ppm`
- **Data type**: `int`
- **Valid values**: A positive integer representing the zinc content of the hay sample in parts per million (PPM). Typical values range from `20` to `50 PPM`; values below `30 PPM` may indicate marginal zinc availability.

<details>
  <summary>More about <code>zinc_ppm</code></summary>

  <p>Zinc (Zn) is an essential trace mineral involved in enzyme function, immune response, wound healing, and reproductive performance. Forage zinc levels are commonly marginal or deficient, especially in high-calcium or high-iron environments where mineral interactions reduce bioavailability.</p>

  <p>Zinc is reported in parts per million (PPM) on a dry matter basis. Most forages fall between <code>20</code> and <code>50 PPM</code>. Levels below <code>30 PPM</code> may be inadequate for optimal livestock performance and often require supplementation.</p>

  <p>Monitoring zinc is especially important in young growing animals, breeding stock, and high-producing dairy cows.</p>

</details>

#### `copper_ppm`
- **Data type**: `int`
- **Valid values**: A positive integer representing the copper content of the hay sample in parts per million (PPM). Typical values range from `5` to `15 PPM`; values below `8 PPM` may be marginal, while values above `20 PPM` may pose toxicity risk, particularly in sheep.

<details>
  <summary>More about <code>copper_ppm</code></summary>

  <p>Copper (Cu) is an essential trace mineral involved in enzyme activity, immune function, connective tissue formation, and pigment synthesis. Copper deficiency is one of the most common trace mineral issues in forage-fed livestock, particularly in areas with high soil iron, sulfur, or molybdenum.</p>

  <p>Forage copper is reported in parts per million (PPM) on a dry matter basis. Most hays contain between <code>5</code> and <code>15 PPM</code>. Levels below <code>8 PPM</code> are often considered marginal and may require supplementation. However, levels above <code>20 PPM</code> can be toxic to sheep and should be evaluated carefully for species-specific feeding.</p>

  <p>Mineral interactions should be considered when interpreting forage copper values. Supplemental copper should be based on total dietary antagonistic load, not forage concentration alone.</p>

</details>

#### `manganese_ppm`
- **Data type**: `int`
- **Valid values**: A positive integer representing the manganese content of the hay sample in parts per million (PPM). Typical values range from `40` to `300 PPM`. Values below `40 PPM` may be inadequate; values above `400 PPM` are uncommon but generally not toxic.

<details>
  <summary>More about <code>manganese_ppm</code></summary>

  <p>Manganese (Mn) is a trace mineral critical for skeletal development, reproductive health, and antioxidant enzyme function. Although many forages contain high levels of manganese, its bioavailability is low, and absorption is further reduced by high iron or calcium levels in the diet.</p>

  <p>Forage manganese is measured in parts per million (PPM) on a dry matter basis. Most hays contain between <code>40</code> and <code>300 PPM</code>. Levels below <code>40 PPM</code> may warrant supplementation in growing or breeding animals, particularly when forage iron is elevated.</p>

  <p>There is low risk of toxicity, even at elevated forage manganese levels, though excessive Mn can contribute to mineral imbalances. Forage analysis should be considered alongside total dietary load and antagonist levels.</p>

</details>

#### `molybdenum_ppm`
- **Data type**: `float`
- **Valid values**: A positive decimal value representing the molybdenum content of the hay sample in parts per million (PPM). Typical values are less than `2.0 PPM`; values above `3.0 PPM` may antagonize copper absorption in ruminants.

<details>
  <summary>More about <code>molybdenum_ppm</code></summary>

  <p>Molybdenum (Mo) is a trace mineral required in very small amounts for enzyme activity in livestock. However, excess molybdenum can form thiomolybdate compounds in the rumen, which bind to copper and inhibit its absorption, leading to secondary copper deficiency.</p>

  <p>Forage molybdenum is reported in parts per million (PPM) on a dry matter basis. Most forages contain less than <code>2.0 PPM</code>. Concentrations above <code>3.0 PPM</code> — especially when sulfur is also elevated — may contribute to copper antagonism. Values above <code>5.0 PPM</code> are generally considered high risk for ruminants, particularly cattle and sheep.</p>

  <  <p>This field is important for diagnosing trace mineral imbalances and planning appropriate supplementation strategies. When molybdenum levels are elevated, especially in combination with high sulfur, it may be necessary to increase dietary copper or use chelated mineral forms to ensure adequate absorption.</p>

  </details>

## References

- 302 KAR 37:010. [Standard Hay Grading Program for the State of Kentucky](https://apps.legislature.ky.gov/law/kar/302/037/010.pdf) [PDF]. Retrieved June 19, 2018.

- Baker, R. and S. Ball. 2011. [Variations in Alfalfa Hay Grading](http://lubbock.tamu.edu/files/2011/10/nmsugrading_10.pdf) [PDF]. New Mexico State University Cooperative Extension Service, Guide A-329. Retrieved June 19, 2018.

- Ball, D.M., M. Collins, G.D. Lacefield, N.P. Martin, D.A. Mertens, K.E. Olson, D.H. Putnam, D.J. Undersander, and M.W. Wolf. 2001. [Understanding Forage Quality](https://fyi.extension.wisc.edu/forage/files/2017/04/FQ.pdf) [PDF]. Also archived at: [https://web.archive.org/web/20250424/https://fyi.extension.wisc.edu/forage/files/2017/04/FQ.pdf](https://web.archive.org/web/20250424/https://fyi.extension.wisc.edu/forage/files/2017/04/FQ.pdf) American Farm Bureau Federation Publication 1-01, Park Ridge, IL, via National Forage Testing Association. Retrieved April 24, 2025.

- Bates, G. [High Quality Hay Production](https://shelbycountytn.gov/DocumentCenter/View/1183/High-Quality-Hay-Production?bidId=) [PDF]. University of Tennessee Agricultural Extension Service Publication SP 437-A. Retrieved June 19, 2018.

- Canadian Food Inspection Agency. 2013. D-03-14: [Canadian Hay Certification Program to certify hay for export](https://inspection.canada.ca/plant-health/invasive-species/directives/grains-and-field-crops/d-03-14/eng/1323829800901/1323829873124). Retrieved June 19, 2018.

- Carolina Farm Stewardship Association. [Organic and Non-GMO Feed and Hay Sources Finder](https://www.carolinafarmstewards.org/organic-and-non-gmo-feed-and-hay-sources-for-the-carolinas/). Retrieved June 19, 2018.

- Corriher, V., T. Provin, and L. Redmon. 2010. [Hay Production in Texas](http://soiltesting.tamu.edu/publications/E-273.pdf) [PDF]. Texas A&M AgriLife Extension, E-273. Retrieved June 19, 2018.

- Corriher, V. and L. Redmon. 2009. [Bermudagrass Varieties, Hybrids and Blends for Texas](http://publications.tamu.edu/FORAGE/PUB_forage_Bermudagrass%20Varieties.pdf) [PDF]. Texas A&M AgriLife Extension, SCS-2009-11. Retrieved June 19, 2018.

- Guerrero, J. 2001. [Marketing Standards for Southern California Grass Export Hay](https://alfalfa.ucdavis.edu/+symposium/proceedings/2001/01-207.pdf) [PDF]. University of California Cooperative Extension. Retrieved June 19, 2018.

- Lawrence, L. and R. Coleman. 2000. [Choosing Hay for Horses](http://www2.ca.uky.edu/agcomm/pubs/id/id146/id146.pdf) [PDF]. University of Kentucky Cooperative Extension Service, ID-146. Retrieved June 19, 2018.

- Marsalis, M., G. Hagevoort, and L. Lauriault. 2009. [Hay Quality, Sampling, and Testing](https://aces.nmsu.edu/pubs/_circulars/CR641/). New Mexico State University Cooperative Extension Service, Circular 641. Retrieved June 19, 2018.

- National Alfalfa Alliance. [Alfalfa: The High Quality Hay for Horses](http://www.alfalfa.org/pdf/Alfalfa%20for%20Horses%20(low%20res).pdf) [PDF]. Retrieved June 19, 2018.

- Putnam, D. 2010. [Changing Forage Quality Testing for Alfalfa Hay Markets](https://alfalfa.ucdavis.edu/+symposium/2010/files/talks/CAS24_PutnamQualityMarkets.pdf) [PDF]. University of California Department of Plant Sciences (UC Davis). Retrieved June 19, 2018.

- Putnam, D. 2003. [Recommended Principles for Proper Hay Sampling](https://wolfe.ca.uky.edu/files/principals_for_proper_hay_testing.pdf) [PDF]. University of California, Davis, via National Forage Testing Association. Retrieved June 19, 2018.

- Provin, T. and J. Pitt. 2002. [Sampling Hay Bales and Pastures for Forage Analysis](http://ward.agrilife.org/files/2011/07/tmppdfs_45776-e148.pdf) [PDF]. Texas A&M AgriLife Extension, E-148. Retrieved June 19, 2018.

## Acknowledgments

The development of this hay specification was informed by a wide body of extension publications, academic resources, producer feedback, and laboratory testing practices. We gratefully acknowledge the contributions of:

- Agricultural extension specialists and researchers from universities across the United States, including Texas A&M, University of Kentucky, University of California Davis, and New Mexico State University.
- The National Forage Testing Association (NFTA) and member laboratories for promoting consistent, science-based forage analysis practices.
- Industry professionals and producers who shared their insights into real-world hay production, marketing, and quality assurance needs.

Special thanks to the authors of the publications cited above, whose work continues to shape best practices in forage evaluation.

## Licensing notice

This specification is provided for public use and may be implemented freely by producers, buyers, software developers, and standards organizations under the terms of the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Under this license, you are free to:

- **Share** — copy and redistribute the material in any medium or format  
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially  

**Under the following terms:**

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

To contribute improvements or extensions to this specification, or to report implementation experiences, please contact the maintainers via email at [standards@lode.global](mailto:standards@lode.global).

---

## Contact

This specification is published by **Lode**, a provider of information, logistics, and trading support for agricultural commodities.

For questions, feedback, or to request implementation guidance, please contact:

**Lode Standards Team**  
📧 [standards@lode.global](mailto:standards@lode.global)  
🌐 [https://lode.global](https://lode.global)

We welcome inquiries from producers, merchants, buyers, researchers, industry groups, and software providers seeking to adopt or integrate this standard.
