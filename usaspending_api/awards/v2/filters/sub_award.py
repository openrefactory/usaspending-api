import itertools
import logging

from django.db.models import Q

from usaspending_api.awards.models_matviews import SubawardView
from usaspending_api.awards.v2.filters.location_filter_geocode import geocode_filter_locations
from usaspending_api.awards.v2.lookups.lookups import contract_type_mapping
from usaspending_api.common.exceptions import InvalidParameterException
from usaspending_api.references.models import PSC
from usaspending_api.search.v2 import elasticsearch_helper
from .filter_helpers import date_or_fy_queryset, total_obligation_queryset
logger = logging.getLogger(__name__)


# TODO: Performance when multiple false values are initially provided
def subaward_filter(filters):

    queryset = SubawardView.objects.all()
    for key, value in filters.items():

        if value is None:
            raise InvalidParameterException('Invalid filter: ' + key + ' has null as its value.')

        key_list = [
            'keywords',
            'elasticsearch_keyword',
            'time_period',
            'award_type_codes',
            'agencies',
            'legal_entities',
            'recipient_search_text',
            'recipient_scope',
            'recipient_locations',
            'recipient_type_names',
            'place_of_performance_scope',
            'place_of_performance_locations',
            'award_amounts',
            'award_ids',
            'program_numbers',
            'naics_codes',
            'psc_codes',
            'contract_pricing_type_codes',
            'set_aside_type_codes',
            'extent_competed_type_codes'
        ]

        if key not in key_list:
            raise InvalidParameterException('Invalid filter: ' + key + ' does not exist.')

        if key == "keywords":
            def keyword_parse(keyword):
                # keyword_ts_vector & award_ts_vector are Postgres TS_vectors.
                # keyword_ts_vector = recipient_name + psc_description + subaward_description
                # award_ts_vector = piid + fain + uri + subaward_number
                filter_obj = Q(keyword_ts_vector=keyword) | \
                    Q(award_ts_vector=keyword)
                if keyword.isnumeric():
                    filter_obj |= Q(naics_code__contains=keyword)
                if len(keyword) == 4 and PSC.objects.all().filter(code__iexact=keyword).exists():
                    filter_obj |= Q(product_or_service_code__iexact=keyword)

                return filter_obj

            filter_obj = Q()
            for keyword in value:
                filter_obj |= keyword_parse(keyword)
            potential_DUNS = list(filter((lambda x: len(x) > 7 and len(x) < 10), value))
            if len(potential_DUNS) > 0:
                filter_obj |= Q(recipient_unique_id__in=potential_DUNS) | \
                    Q(parent_recipient_unique_id__in=potential_DUNS)

            queryset = queryset.filter(filter_obj)

        elif key == "elasticsearch_keyword":
            keyword = value
            transaction_ids = elasticsearch_helper.get_download_ids(keyword=keyword, field='transaction_id')
            # flatten IDs
            transaction_ids = list(itertools.chain.from_iterable(transaction_ids))
            logger.info('Found {} transactions based on keyword: {}'.format(len(transaction_ids), keyword))
            transaction_ids = [str(transaction_id) for transaction_id in transaction_ids]
            queryset = queryset.filter(latest_transaction_id__isnull=False)
            queryset &= queryset.extra(
                where=['"latest_transaction_id" = ANY(\'{{{}}}\'::int[])'.format(','.join(transaction_ids))])

        elif key == "time_period":
            # TODO- Handle both "action_date" and "last_modified_date"
            success, or_queryset = date_or_fy_queryset(value, SubawardView, "fiscal_year", "action_date")
            if success:
                queryset &= or_queryset

        elif key == "award_type_codes":
            idv_flag = all(i in value for i in contract_type_mapping.keys())

            if len(value) != 0:
                filter_obj = Q(prime_award_type__in=value)
                if idv_flag:
                    filter_obj |= Q(pulled_from='IDV')
                queryset &= SubawardView.objects.filter(filter_obj)

        elif key == "agencies":
            # TODO: Make function to match agencies in award filter throwing dupe error
            funding_toptier = Q()
            funding_subtier = Q()
            awarding_toptier = Q()
            awarding_subtier = Q()
            for v in value:
                type = v["type"]
                tier = v["tier"]
                name = v["name"]
                if type == "funding":
                    if tier == "toptier":
                        funding_toptier |= Q(funding_toptier_agency_name=name)
                    elif tier == "subtier":
                        if 'toptier_name' in v:
                            funding_subtier |= (Q(funding_subtier_agency_name=name) &
                                                Q(funding_toptier_agency_name=v['toptier_name']))
                        else:
                            funding_subtier |= Q(funding_subtier_agency_name=name)

                elif type == "awarding":
                    if tier == "toptier":
                        awarding_toptier |= Q(awarding_toptier_agency_name=name)
                    elif tier == "subtier":
                        if 'toptier_name' in v:
                            awarding_subtier |= (Q(awarding_subtier_agency_name=name) &
                                                 Q(awarding_toptier_agency_name=v['toptier_name']))
                        else:
                            awarding_subtier |= Q(awarding_subtier_agency_name=name)

            awarding_queryfilter = Q()
            funding_queryfilter = Q()

            # Since these are Q filters, no DB hits for boolean checks
            if funding_toptier:
                funding_queryfilter |= funding_toptier
            if funding_subtier:
                funding_queryfilter |= funding_subtier
            if awarding_toptier:
                awarding_queryfilter |= awarding_toptier
            if awarding_subtier:
                awarding_queryfilter |= awarding_subtier

            queryset = queryset.filter(funding_queryfilter & awarding_queryfilter)

        elif key == "legal_entities":
            # This filter key has effectively become obsolete by recipient_search_text
            msg = 'API request included "{}" key. No filtering will occur with provided value "{}"'
            logger.info(msg.format(key, value))
            # or_queryset = []
            # for v in value:
            #     or_queryset.append(v)
            # if len(or_queryset) != 0:
            #     queryset &= SubawardView.objects.filter(recipient__legal_entity_id__in=or_queryset)

        elif key == "recipient_search_text":
            def recip_string_parse(recipient_string):
                upper_recipient_string = str(value[0]).upper()

                # recipient_name_ts_vector is a postgres TS_Vector
                filter_obj = Q(recipient_name_ts_vector=upper_recipient_string)
                if len(upper_recipient_string) == 9 and upper_recipient_string[:5].isnumeric():
                    filter_obj |= Q(recipient_unique_id=upper_recipient_string)
                return filter_obj

            filter_obj = Q()
            for recip in value:
                filter_obj |= recip_string_parse(recip)
            queryset &= SubawardView.objects.filter(filter_obj)

        elif key == "recipient_scope":
            if value == "domestic":
                queryset = queryset.filter(recipient_location_country_name="UNITED STATES")
            elif value == "foreign":
                queryset = queryset.exclude(recipient_location_country_name="UNITED STATES")
            else:
                raise InvalidParameterException('Invalid filter: recipient_scope type is invalid.')

        elif key == "recipient_locations":
            or_queryset = geocode_filter_locations(
                'recipient_location', value, SubawardView, True
            )
            queryset &= or_queryset

        elif key == "recipient_type_names":
            if len(value) != 0:
                queryset &= SubawardView.objects.filter(business_categories__overlap=value)

        elif key == "place_of_performance_scope":
            if value == "domestic":
                queryset = queryset.filter(pop_country_name="UNITED STATES")
            elif value == "foreign":
                queryset = queryset.exclude(pop_country_name="UNITED STATES")
            else:
                raise InvalidParameterException('Invalid filter: place_of_performance_scope is invalid.')

        elif key == "place_of_performance_locations":
            queryset &= geocode_filter_locations(
                'pop', value, SubawardView, True
            )

        elif key == "award_amounts":
            queryset &= total_obligation_queryset(value, SubawardView, filters)

        elif key == "award_ids":
            filter_obj = Q()
            for val in value:
                # award_id_string is a Postgres TS_vector
                # award_id_string = piid + fain + uri + subaward_number
                filter_obj |= Q(award_ts_vector=val)
            queryset &= SubawardView.objects.filter(filter_obj)

        # add "naics_codes" (column naics) after NAICS are mapped to subawards
        elif key in ("program_numbers", "psc_codes", "contract_pricing_type_codes"):
            filter_to_col = {
                "program_numbers": "cfda_number",
                "psc_codes": "product_or_service_code",
                "contract_pricing_type_codes": "type_of_contract_pricing",
            }
            in_query = [v for v in value]
            if len(in_query) != 0:
                queryset &= SubawardView.objects.filter(**{'{}__in'.format(filter_to_col[key]): in_query})

        elif key in ("set_aside_type_codes", "extent_competed_type_codes"):
            or_queryset = Q()
            filter_to_col = {
                "set_aside_type_codes": "type_set_aside",
                "extent_competed_type_codes": "extent_competed",
            }
            in_query = [v for v in value]
            for v in value:
                or_queryset |= Q(**{'{}__exact'.format(filter_to_col[key]): in_query})
            queryset = queryset.filter(or_queryset)

    return queryset
