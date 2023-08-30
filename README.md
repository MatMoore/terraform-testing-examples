# Testing terraform examples

Examples of "unit" testing terraform deployments.

Such tests actually deploy a terraform module and then verify the result. For example, you can verify that a service returns a 200 response.

The goal of this repo is to evaluate some of the tools for unit testing infrastructure. See also [adopting_terraform_testing.md](./adopting_terraform_testing.md) for a checklist for actually adopting one of these tools into an existing delivery pipeline.

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


### Writing new tests

Tests live in files like *_test.go.

The core of each test looks like this:

```go
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../examples/terraform-aws-hello-world-example",
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

    // ... make some assertions
```

To make the test stronger, you can swap out `InitAndApply` for `InitAndApplyIdempotent`, which applies the terraform module twice, and checks nothing changes.

There are different ways to assert against things in the test:

- Directly assert that module outputs (e.g. domains, IPs) match expected values
- Retrieve IDs of AWS resources and interract with them via the [aws subpackage](https://pkg.go.dev/github.com/gruntwork-io/terratest@v0.43.13/modules/aws) ([example 1](https://github.com/gruntwork-io/terratest/blob/v0.43.13/test/terraform_aws_rds_example_test.go) [example 2](https://github.com/gruntwork-io/terratest/blob/v0.43.13/test/terraform_aws_s3_example_test.go)) (only possible for some services)
- Retrieve an IP/Domain and issue an HTTP request, as in [terraform_aws_hello_world_example_test](./test/terraform_aws_hello_world_example_test.go) 