# Testing terraform examples

Examples of "unit" testing terraform deployments.

Such tests actually deploy a terraform module and then verify the result. For example, you can verify that a service returns a 200 response.

## Prerequisites

Make sure [terraform](https://developer.hashicorp.com/terraform/downloads?product_intent=terraform) is installed and available on the path.

## Testing with Terratest

These tests are written in Go. It can test terraform in addition to other things, like docker containers.

### Prerequisites

[Install go](https://golang.org/).

Configure dependencies:

```
cd test
go mod init "github.com/MatMoore/terraform-testing-examples"
go mod tidy
```

### Run tests

```
cd test
go test -v -timeout 30m
```

Warning: If the test times out, the terraform destroy will not run, and you will have hanging resources!

### Test descriptions

#### [terraform_basic_example_test](./test/terraform_basic_example_test.go) 
This test does not use any external providers, so the test just applies the plan and asserts against the outputs.

#### [terraform_aws_hello_world_example_test](./test/terraform_aws_hello_world_example_test.go) 
This test deploys a resource to AWS.

[You will need credentials configured to run the test.](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration)

The test applies the plan and retrieves the IP of the web server from the output. Then it queries the server to check it is running as expected.