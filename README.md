# Testing terraform examples

Examples of "unit" testing terraform deployments.

Such tests actually deploy a terraform module and then verify the result. For example, you can verify that a service returns a 200 response.

## Prerequisites

We need terraform installed and on the path.

## Terratest

These tests are written in Go.

## Prerequisites

[Install go](https://golang.org/).

Configure dependencies:

```
cd test
go mod init "github.com/MatMoore/terraform-testing-examples"
go mod tidy
```

## Run tests

```
cd test
go test -v -timeout 30m
```