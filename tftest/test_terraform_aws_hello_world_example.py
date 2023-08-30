import pytest
import tftest
import requests


@pytest.fixture(scope="module")
def output(fixtures_dir):
  tf = tftest.TerraformTest('terraform-aws-hello-world-example', fixtures_dir)
  tf.setup()
  tf.apply(output=True)

  yield tf.output()
  
  tf.destroy(**{"auto_approve": True})


def test_outputs(output):
  public_ip = output['public_ip']
  response = requests.get(f"http://{public_ip}")
  assert response.status_code == 200