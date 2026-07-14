from api.features import API_FEATURE_SPECS


def test_api_feature_registry_declares_auth_and_payments_features():
    assert [feature.feature_id for feature in API_FEATURE_SPECS] == ["auth", "payments"]
