# Testing terraform examples

Examples of "unit" testing terraform deployments.

Such tests actually deploy a terraform module and then verify the result. For example, you can verify that a service returns a 200 response.

## Prerequisites

Make sure [terraform](https://developer.hashicorp.com/terraform/downloads?product_intent=terraform) is installed and available on the path.

## Testing with Terratest

These tests are written in Go.

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

### Test descriptions

#### [terraform_basic_example_test](./test/terraform_basic_example_test.go) 
This test does not use any external providers, so the test just applies the plan and asserts against the outputs.