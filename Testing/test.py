import pytest

@pytest.mark.parametrize("foo,bar", [
  (1, 1),
  (2, 2),
  (3, 3),
])
def test_true(foo, bar):
  assert foo == bar