import pytest
from django.urls import reverse
from django.db import connection
from products.models import Product, Brand, Category

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")

@pytest.fixture
def brand(db):
    return Brand.objects.create(name="Nestle", name_ar="نستله")

@pytest.fixture
def category(db):
    return Category.objects.create(name="Dairy", name_ar="منتجات الألبان")

@pytest.fixture
def product(brand, category):
    return Product.objects.create(
        name="Milk",
        name_ar="حليب",
        brand=brand,
        category=category,
        nutrition_facts={"calories": 150, "fat": 8}
    )

@pytest.mark.django_db
def test_search_english(client, product):
    url = reverse('product-search') + '?q=milk'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['name'] == 'Milk'

@pytest.mark.django_db
def test_search_arabic(client, product):
    url = reverse('product-search') + '?q=حليب'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['name_ar'] == 'حليب'

@pytest.mark.django_db
def test_search_mixed_query(client, product):
    url = reverse('product-search') + '?q=milk حليب'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['name'] == 'Milk'
    assert results[0]['name_ar'] == 'حليب'

@pytest.mark.django_db
def test_search_misspelling_english(client, product):
    url = reverse('product-search') + '?q=melk'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['name'] == 'Milk'

@pytest.mark.django_db
def test_search_misspelling_arabic(client, product):
    url = reverse('product-search') + '?q=حلييب'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['name_ar'] == 'حليب'

@pytest.mark.django_db
def test_filter_by_category(client, product, category):
    url = reverse('product-search') + f'?q=milk&category_id={category.id}'
    response = client.get(url)
    assert response.status_code == 200
    results = response.json()['results']
    assert len(results) == 1
    assert results[0]['category']['id'] == category.id