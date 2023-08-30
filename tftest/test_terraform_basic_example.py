import pytest
import tftest


@pytest.fixture(scope="module")
def output(fixtures_dir):
  tf = tftest.TerraformTest('terraform-basic-example', fixtures_dir)
  tf.setup()
  tf.apply(output=True)

  yield tf.output()
  
  tf.destroy(**{"auto_approve": True})


def test_outputs(output):
  assert output['example'] == 'example'
  assert output['example_list'] == []
  assert output['example_map'] == {}
