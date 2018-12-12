import vcr
from pytest import fixture
from mercadolibre.pyme import PyMe

@fixture
def user_keys():
    # keys that need to return from user
    return ['id', 'nickname', 'registration_date', 'country_id', 'address',
            'user_type', 'tags', 'logo', 'points', 'site_id', 'permalink',
            'seller_reputation', 'buyer_reputation', 'status']

@vcr.use_cassette('tests/vcr_cassettes/user-info.yml' filter_query_parameters=['api_key'])
def test_user_info(user_keys):
    """Tests an API call to get a user info"""

    pyme_instance = PyMe(206946886)
    response = pyme_instance.display()

    assert isinstance(response, dict)
    assert response['id'] == 206946886, "The ID of the user should be in the response"
    assert set(user_keys).issubset(response.keys()), "All keys should be in the response"
