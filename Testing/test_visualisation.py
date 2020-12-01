import pytest
from BackEnd.functions.visualisation import DataVisualiser


@pytest.fixture
def get_visualiser():
    return DataVisualiser()


@pytest.mark.parametrize("test_cloud", {
    'vaccine': 24.494451921365844,
    'vaccines': 17.246587320931177,
    'vaccination': 14.422064752849082,
    'eu': 13.07498794836623,
    'confidence': 12.499278008676121,
    'health': 10.120849876619543,
    'influenza': 9.491345599998128,
    'survey': 9.436829705712428,
    'countries': 8.057116597421519,
    'member': 7.320234856880347,
    'country': 7.132522234768666,
    'safety': 6.925794706351324,
    'uk': 6.461624317321705,
    'mmr': 6.253096584219371,
    'media': 6.18232732275487,
    'group': 6.051261614005282,
    'gps': 5.600060767464086,
    'latest': 5.344915675353408,
    'people': 5.285584305514587,
    'data': 5.237241166041486,
    'measles': 5.111472710107966,
    'news': 5.094144139515012,
    'groups': 5.0169148796798355,
    'children': 4.995421888472756,
    'states': 4.891921107755419})
def test_word_cloud(test_cloud, get_visualiser):
    assert test_cloud == get_visualiser('some_random_hash')
