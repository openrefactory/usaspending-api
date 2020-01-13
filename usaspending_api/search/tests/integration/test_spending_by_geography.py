import json
import pytest

from rest_framework import status
from usaspending_api.search.tests.data.search_filters_test_data import non_legacy_filters


@pytest.mark.django_db
def test_spending_by_geography_state_success(client):
    # test for required filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "state",
                "filters": {"recipient_locations": [{"country": "ABC"}]},
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK

    # test all filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "recipient_location",
                "geo_layer": "county",
                "geo_layer_filters": ["WA"],
                "filters": non_legacy_filters(),
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_spending_by_geography_county_success(client):
    # test for required filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "county",
                "filters": {"recipient_locations": [{"country": "ABC"}]},
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK

    # test all filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "recipient_location",
                "geo_layer": "county",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_spending_by_geography_congressional_success(client):
    # test for required filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "district",
                "filters": {"recipient_locations": [{"country": "ABC"}]},
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK

    # test all filters
    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "recipient_location",
                "geo_layer": "district",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_spending_by_geography_failure(client):
    """Verify error on bad autocomplete request for budget function."""

    resp = client.post(
        "/api/v2/search/spending_by_geography/",
        content_type="application/json",
        data=json.dumps({"scope": "test", "filters": {}}),
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_spending_by_geography_subawards_success(client):

    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "recipient_location",
                "geo_layer": "county",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
                "subawards": True,
            }
        ),
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_spending_by_geography_subawards_failure(client):

    resp = client.post(
        "/api/v2/search/spending_by_geography",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "recipient_location",
                "geo_layer": "county",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
                "subawards": "string",
            }
        ),
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.skip
@pytest.mark.django_db
def test_spending_by_geography_incorrect_state(client):
    resp = client.post(
        "/api/v2/search/spending_by_geography/",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "state",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
            }
        ),
    )

    assert resp.data["results"][0]["display_name"] in ["Alabama", "None"]


@pytest.mark.skip
@pytest.mark.django_db
def test_spending_by_geography_incorrect_county(client):
    resp = client.post(
        "/api/v2/search/spending_by_geography/",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "county",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
            }
        ),
    )
    # raise Exception(resp.content)
    assert resp.data["results"][0]["display_name"] == "County"


@pytest.mark.django_db
def test_spending_by_geography_incorrect_district(client):
    resp = client.post(
        "/api/v2/search/spending_by_geography/",
        content_type="application/json",
        data=json.dumps(
            {
                "scope": "place_of_performance",
                "geo_layer": "district",
                "geo_layer_filters": ["01"],
                "filters": non_legacy_filters(),
            }
        ),
    )

    assert len(resp.data["results"]) == 0
