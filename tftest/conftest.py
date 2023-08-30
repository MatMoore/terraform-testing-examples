import os
import pytest


@pytest.fixture(scope='session')
def fixtures_dir():
  return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', 'examples')


@pytest.fixture(scope='session')
def terraform_basic_example_dir(fixtures_dir):
    return fixtures_dir + '/terraform-basic-example'