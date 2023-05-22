from faker import Faker
from tests.conftest import async_client


fake = Faker()


async def test_auth(async_client: async_client):
    """Test auth user"""
    for index in range(1, 5):
        profile = fake.simple_profile()
        username = profile.get('username')
        response = await async_client.post(
            url='/user/auth/',
            json={'username': f'{username}'}
        )
        assert response.status_code == 200
        result = response.json()
        assert result['uuid']