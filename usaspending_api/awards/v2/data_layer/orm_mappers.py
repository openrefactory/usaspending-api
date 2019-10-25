from collections import OrderedDict

# For all *_FIELDS ordered dictionaries:
#  Key:Value => (DB field, API response field)
OFFICER_FIELDS = OrderedDict(
    [
        ("officer_1_name", "_officer_1_name"),
        ("officer_1_amount", "_officer_1_amount"),
        ("officer_2_name", "_officer_2_name"),
        ("officer_2_amount", "_officer_2_amount"),
        ("officer_3_name", "_officer_3_name"),
        ("officer_3_amount", "_officer_3_amount"),
        ("officer_4_name", "_officer_4_name"),
        ("officer_4_amount", "_officer_4_amount"),
        ("officer_5_name", "_officer_5_name"),
        ("officer_5_amount", "_officer_5_amount"),
    ]
)


FABS_AWARD_FIELDS = OrderedDict(
    [
        ("id", "id"),
        ("generated_unique_award_id", "generated_unique_award_id"),
        ("fain", "fain"),
        ("uri", "uri"),
        ("category", "category"),
        ("type", "type"),
        ("type_description", "type_description"),
        ("description", "description"),
        ("subaward_count", "subaward_count"),
        ("total_subaward_amount", "total_subaward_amount"),
        ("awarding_agency", "awarding_agency"),
        ("funding_agency", "funding_agency"),
        ("recipient", "recipient"),
        ("subaward_count", "subaward_count"),
        ("total_subaward_amount", "total_subaward_amount"),
        ("total_subsidy_cost", "total_subsidy_cost"),
        ("total_loan_value", "total_loan_value"),
        ("total_obligation", "total_obligation"),
        ("base_and_all_options_value", "base_and_all_options"),
        ("base_exercised_options_val", "base_exercised_options"),
        ("non_federal_funding_amount", "non_federal_funding"),
        ("total_funding_amount", "total_funding"),
        *OFFICER_FIELDS.items(),
        # extra fields
        ("recipient_id", "_lei"),
        ("latest_transaction_id", "_trx"),
        ("awarding_agency_id", "_awarding_agency"),
        ("funding_agency_id", "_funding_agency"),
        ("period_of_performance_start_date", "_start_date"),
        ("period_of_performance_current_end_date", "_end_date"),
        ("date_signed", "date_signed"),
    ]
)


FPDS_AWARD_FIELDS = OrderedDict(
    [
        ("id", "id"),
        ("generated_unique_award_id", "generated_unique_award_id"),
        ("piid", "piid"),
        ("category", "category"),
        ("type", "type"),
        ("type_description", "type_description"),
        ("description", "description"),
        ("total_obligation", "total_obligation"),
        ("base_exercised_options_val", "base_exercised_options"),
        ("base_and_all_options_value", "base_and_all_options"),
        ("subaward_count", "subaward_count"),
        ("total_subaward_amount", "total_subaward_amount"),
        *OFFICER_FIELDS.items(),
        # extra fields
        ("recipient_id", "_lei"),
        ("latest_transaction_id", "_trx"),
        ("awarding_agency_id", "_awarding_agency"),
        ("funding_agency_id", "_funding_agency"),
        ("period_of_performance_start_date", "_start_date"),
        ("period_of_performance_current_end_date", "_end_date"),
        ("date_signed", "date_signed"),
        ("fpds_parent_agency_id", "_fpds_parent_agency_id"),
        ("parent_award_piid", "_parent_award_piid"),
    ]
)


FABS_ASSISTANCE_FIELDS = OrderedDict(
    [
        ("cfda_number", "cfda_number"),
        ("cfda_title", "cfda_title"),
        ("modified_at", "_modified_at"),
        # "Recipient" fields below
        ("awardee_or_recipient_legal", "_recipient_name"),
        ("awardee_or_recipient_uniqu", "_recipient_unique_id"),
        ("ultimate_parent_legal_enti", "_parent_recipient_name"),
        ("ultimate_parent_unique_ide", "_parent_recipient_unique_id"),
        ("legal_entity_country_code", "_rl_location_country_code"),
        ("legal_entity_country_name", "_rl_country_name"),
        ("legal_entity_state_code", "_rl_state_code"),
        ("legal_entity_city_name", "_rl_city_name"),
        ("legal_entity_county_name", "_rl_county_name"),
        ("legal_entity_address_line1", "_rl_address_line1"),
        ("legal_entity_address_line2", "_rl_address_line2"),
        ("legal_entity_address_line3", "_rl_address_line3"),
        ("legal_entity_congressional", "_rl_congressional_code"),
        ("legal_entity_zip_last4", "_rl_zip4"),
        ("legal_entity_zip5", "_rl_zip5"),
        ("legal_entity_foreign_posta", "_rl_foreign_postal_code"),
        ("legal_entity_foreign_provi", "_rl_foreign_province"),
        # "Place of Performance" fields below
        ("place_of_perform_country_c", "_pop_location_country_code"),
        ("place_of_perform_country_n", "_pop_country_name"),
        ("place_of_perform_county_na", "_pop_county_name"),
        ("place_of_performance_city", "_pop_city_name"),
        ("place_of_perfor_state_code", "_pop_state_code"),
        ("place_of_perform_state_nam", "_pop_state_name"),
        ("place_of_performance_congr", "_pop_congressional_code"),
        ("place_of_perform_zip_last4", "_pop_zip4"),
        ("place_of_performance_zip5", "_pop_zip5"),
        ("place_of_performance_forei", "_pop_foreign_province"),
        ("awarding_office_name", "_awarding_office_name"),
        ("funding_office_name", "_funding_office_name"),
    ]
)


FPDS_CONTRACT_FIELDS = OrderedDict(
    [
        ("idv_type_description", "idv_type_description"),
        ("type_of_idc_description", "type_of_idc_description"),
        ("referenced_idv_agency_iden", "referenced_idv_agency_iden"),
        ("referenced_idv_agency_desc", "referenced_idv_agency_desc"),
        ("multiple_or_single_aw_desc", "multiple_or_single_award_description"),
        ("solicitation_identifier", "solicitation_identifier"),
        ("solicitation_procedures", "solicitation_procedures"),
        ("solicitation_procedur_desc", "solicitation_procedures_description"),
        ("number_of_offers_received", "number_of_offers_received"),
        ("extent_competed", "extent_competed"),
        ("extent_compete_description", "extent_competed_description"),
        ("other_than_full_and_open_c", "other_than_full_and_open"),
        ("other_than_full_and_o_desc", "other_than_full_and_open_description"),
        ("type_set_aside", "type_set_aside"),
        ("type_set_aside_description", "type_set_aside_description"),
        ("commercial_item_acquisitio", "commercial_item_acquisition"),
        ("commercial_item_acqui_desc", "commercial_item_acquisition_description"),
        ("commercial_item_test_progr", "commercial_item_test_program"),
        ("commercial_item_test_desc", "commercial_item_test_program_description"),
        ("evaluated_preference", "evaluated_preference"),
        ("evaluated_preference_desc", "evaluated_preference_description"),
        ("fed_biz_opps", "fed_biz_opps"),
        ("fed_biz_opps_description", "fed_biz_opps_description"),
        ("small_business_competitive", "small_business_competitive"),
        ("fair_opportunity_limited_s", "fair_opportunity_limited"),
        ("fair_opportunity_limi_desc", "fair_opportunity_limited_description"),
        ("product_or_service_code", "product_or_service_code"),
        ("product_or_service_co_desc", "product_or_service_description"),
        ("naics", "naics"),
        ("naics_description", "naics_description"),
        ("dod_claimant_program_code", "dod_claimant_program"),
        ("dod_claimant_prog_cod_desc", "dod_claimant_program_description"),
        ("program_system_or_equipmen", "dod_acquisition_program"),
        ("program_system_or_equ_desc", "dod_acquisition_program_description"),
        ("information_technology_com", "information_technology_commercial_item_category"),
        ("information_technolog_desc", "information_technology_commercial_item_category_description"),
        ("sea_transportation", "sea_transportation"),
        ("sea_transportation_desc", "sea_transportation_description"),
        ("clinger_cohen_act_planning", "clinger_cohen_act_planning"),
        ("clinger_cohen_act_pla_desc", "clinger_cohen_act_planning_description"),
        ("construction_wage_rate_req", "construction_wage_rate"),
        ("construction_wage_rat_desc", "construction_wage_rate_description"),
        ("labor_standards", "labor_standards"),
        ("labor_standards_descrip", "labor_standards_description"),
        ("materials_supplies_article", "materials_supplies"),
        ("materials_supplies_descrip", "materials_supplies_description"),
        ("cost_or_pricing_data", "cost_or_pricing_data"),
        ("cost_or_pricing_data_desc", "cost_or_pricing_data_description"),
        ("domestic_or_foreign_entity", "domestic_or_foreign_entity"),
        ("domestic_or_foreign_e_desc", "domestic_or_foreign_entity_description"),
        ("foreign_funding", "foreign_funding"),
        ("foreign_funding_desc", "foreign_funding_description"),
        ("interagency_contracting_au", "interagency_contracting_authority"),
        ("interagency_contract_desc", "interagency_contracting_authority_description"),
        ("major_program", "major_program"),
        ("price_evaluation_adjustmen", "price_evaluation_adjustment"),
        ("program_acronym", "program_acronym"),
        ("subcontracting_plan", "subcontracting_plan"),
        ("subcontracting_plan_desc", "subcontracting_plan_description"),
        ("multi_year_contract", "multi_year_contract"),
        ("multi_year_contract_desc", "multi_year_contract_description"),
        ("purchase_card_as_payment_m", "purchase_card_as_payment_method"),
        ("purchase_card_as_paym_desc", "purchase_card_as_payment_method_description"),
        ("consolidated_contract", "consolidated_contract"),
        ("consolidated_contract_desc", "consolidated_contract_description"),
        ("type_of_contract_pricing", "type_of_contract_pricing"),
        ("type_of_contract_pric_desc", "type_of_contract_pricing_description"),
        ("last_modified", "_last_modified"),
        ("period_of_perf_potential_e", "_period_of_perf_potential_e"),
        # "Recipient" fields below
        ("awardee_or_recipient_legal", "_recipient_name"),
        ("awardee_or_recipient_uniqu", "_recipient_unique_id"),
        ("ultimate_parent_legal_enti", "_parent_recipient_name"),
        ("ultimate_parent_unique_ide", "_parent_recipient_unique_id"),
        ("legal_entity_country_code", "_rl_location_country_code"),
        ("legal_entity_country_name", "_rl_country_name"),
        ("legal_entity_state_code", "_rl_state_code"),
        ("legal_entity_city_name", "_rl_city_name"),
        ("legal_entity_county_name", "_rl_county_name"),
        ("legal_entity_address_line1", "_rl_address_line1"),
        ("legal_entity_address_line2", "_rl_address_line2"),
        ("legal_entity_address_line3", "_rl_address_line3"),
        ("legal_entity_congressional", "_rl_congressional_code"),
        ("legal_entity_zip_last4", "_rl_zip4"),
        ("legal_entity_zip5", "_rl_zip5"),
        # "Place of Performance Location"
        ("place_of_perform_country_c", "_pop_location_country_code"),
        ("place_of_perf_country_desc", "_pop_country_name"),
        ("place_of_performance_state", "_pop_state_code"),
        ("place_of_perfor_state_desc", "_pop_state_name"),
        ("place_of_perform_city_name", "_pop_city_name"),
        ("place_of_perform_county_na", "_pop_county_name"),
        ("place_of_perform_zip_last4", "_pop_zip4"),
        ("place_of_performance_congr", "_pop_congressional_code"),
        ("place_of_performance_zip5", "_pop_zip5"),
        ("awarding_office_name", "_awarding_office_name"),
        ("funding_office_name", "_funding_office_name"),
    ]
)
