import pytest
from BackEnd.functions.causal import Causal


@pytest.fixture
def get_causal():
    return Causal()

def test_causal(get_causal):
    keywords = ['Vaccine', 'Vaccination', 'Control', 'Government', 'MicroChip']
    uk_econ, uk_health, uk_politics = get_causal.analyse(keywords, 'United Kingdom')
    #us_econ, us_health, us_politics = get_causal.analyse(keywords, 'United States')
    assert uk_econ.value >= 210.00 #and us_health.value >= 210.00

