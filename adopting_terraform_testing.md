# Considerations when adopting terraform unit testing

This document lists things to consider when adopting a tool like terratest to an existing infrastructure.

## 1. Decide when to use this kind of testing

This testing should complement other tooling, such as linters, or monitoring of services in production.

Infrastructure unit tests are designed to run as part of a continuous integration process when making changes to the terraform code, to give a high degree of confidence before doing a full deploy.

Compared to application unit tests, these are going to be relatively slow (since they actually deploy stuff), so you may want to use them more sparingly or prioritise just a subset of the infrastructure while trialling the tool.

For more details on how unit testing fits in with other tools, see [Automated Testing for Terraform, Docker, Packer, Kubernetes, and More](https://youtu.be/xhHOW0EF5u8?si=_l_Jero1i6oFKygV).

### Checklist

- [ ] Decide at a high level what should and shouldn't have unit test coverage

## 2. Make sure terraform modules are the right granularity

When using these tools, the unit under test is a terraform module, so there is a fundamental assumption that your terraform code is factored into small modules.

If modules are too big, then every time a test runs, it will spin up a lot of unnecessary infrastructure, which will be slower and more brittle.

### Checklist

- [ ] Identify the exact modules to test
- [ ] Verify related functionality is cohesive (not split over too many modules)
- [ ] Verify modules do not contain multiple unrelated components
- [ ] Refactor where appropriate

## 3. Make sure environment specific details can be injected

[These tests are designed to be run in an isolated environment](https://terratest.gruntwork.io/docs/testing-best-practices/testing-environment/). Either a self-contained environment such as [localstack](https://localstack.cloud/) or a separate AWS account (isolated from production and any non-production environments that have other uses).

The consequence is that we cannot have any hardcoded account ids, IP addresses, domain names etc.

### Checklist

- [ ] Identify any environment specific values that are hardcoded
- [ ] Ensure such values can be dependency injected (e.g. through variables and outputs)

## 4. Decide how to provision the testing environment
With localstack, it seems like we can spin up the environment, run the tests, and then tear it down again (TBC). 

However, localstack supports AWS services to varying degrees: see https://docs.localstack.cloud/user-guide/aws/feature-coverage/ - so it may not be possible to use localstack for everything - in such case we have to fall back to using a real AWS account.

Some services are only supported by the Pro version e.g. API Gateway V2. So you need to sort out a license to use it.

It seems like [there is always a risk that resources are left hanging around in persistent test environments](https://terratest.gruntwork.io/docs/testing-best-practices/cleanup/)

Gruntwork recommend a tool called [cloud-nuke](https://github.com/gruntwork-io/cloud-nuke) to wipe the environment nightly.

### Checklist
- [ ] Decide whether localstack should be used for testing all modules/some of them/none of them
- [ ] Obtain a licence if using localstack pro features
- [ ] If using a persistent environment, make sure there is a way to wipe resources periodically


## Things specific to terratest

### Checklist
- [ ] Ensure you are using long timeouts
- [ ] [Deal with interleaved log outputs](https://terratest.gruntwork.io/docs/testing-best-practices/debugging-interleaved-test-output/)
- [ ] [Make sure you are aware of the default test caching behaviour in Go](https://terratest.gruntwork.io/docs/testing-best-practices/avoid-test-caching/)
