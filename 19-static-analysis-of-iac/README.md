# Topic 19: Static Analysis of IAC

<!-- TOC -->

- [Conventions](#conventions)
- [Lesson 19.1: Introduction to cfn_nag](#lesson-191-introduction-to-cfn_nag)
  - [Principle 19.1](#principle-191)
  - [Practice 19.1](#practice-191)
    - [Lab 19.1.1](#lab-1911)
    - [Lab 19.1.2](#lab-1912)
  - [Retrospective 19.1](#retrospective-191)
    - [Question: cfn_nag - Warning vs Fail](#question-cfn_nag-warning-vs-fail)

<!-- /TOC -->

## Conventions

- All CloudFormation templates should be written in YAML.
- Do NOT copy and paste CloudFormation templates from the Internet at large.
- DO use the [CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)
- DO use the [AWS CLI for CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html#)
  (NOT the Console) unless otherwise specified.
- DO use the [cfn_nag documentation](https://github.com/stelligent/cfn_nag#readme)

## Lesson 19.1: Introduction to cfn_nag

### Principle 19.1

The cfn-nag tool looks for patterns in CloudFormation templates
that may indicate insecure infrastructure.
Roughly speaking, it will look for:

- IAM rules that are too permissive (wildcards)
- Security group rules that are too permissive (wildcards)
- Access logs that aren't enabled
- Encryption that isn't enabled
- Password literals

For more background on the tool, please see this post at Stelligent's blog:

[Finding Security Problems Early in the Development Process
of a CloudFormation Template with "cfn-nag"](https://stelligent.com/2016/04/07/finding-security-problems-early-in-the-development-process-of-a-cloudformation-template-with-cfn-nag/)

### Practice 19.1

Use cfn_nag to identify some common security vulnerabilities
in CloudFormation Templates (CFTs)

- IAM Policies
  - Matches policies that are overly permissive in some way
    (e.g. wildcards in actions or principals)

- Security Group ingress and egress rules
  - Matches rules that are overly liberal
    (e.g. absence of an explicit egress rule)

- Encryption
  - Server-side encryption that is not enabled or enforced
    for applicable resources (e.g. Unencrypted EBS volumes)

#### Lab 19.1.1

Code a CloudFormation template that generates a
[CodeBuild Project](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codebuild-project.html)
and its minimal set of requisite resources:

- Add an IAM [execution role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)
  that trusts the CodeBuild service and provides sufficient
  permissions to [deploy cloudformation](https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-custom-role.html).

- Add the [CodeBuild Project](https://github.com/stelligent/stelligent-u/blob/master/19-static-analysis-of-iac/pac/buildspec.yml)
  resource itself, encoding
  - a 'Source' phase to retrieve the code from GitHub
    - Create a [GitHub personal access token](https://github.com/settings/tokens)
      (Connect to this repo since it contains sample cfts
      that demonstrate how cfn_nag works)
  - an 'Install' phase with an action that installs cfn_nag
    in the build environment
  - a 'Build' phase to scan the CFTs in the iac folder of this repo.

Deploy the [Pipeline stack](https://github.com/stelligent/stelligent-u/blob/master/19-static-analysis-of-iac/pac/pipeline.yml)
via the AWS CLI; Note the parameters
that need to be passed to the template
and make sure they are passed through the CLI.

Start the project using [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/codebuild/index.html)
and get the logs (Logs are stored in CloudWatch)

Note the errors in the CFTs in the iac folder that caused the build to fail,
you will need them for the next Lab.

*Note: This repository, in the pac (Pipeline-as-Code) folder
contains the CFT needed to spin up the [CodeBuild Project stack](https://github.com/stelligent/stelligent-u/blob/master/19-static-analysis-of-iac/pac/pipeline.yml)
and the [buildspecs](https://github.com/stelligent/stelligent-u/blob/master/19-static-analysis-of-iac/pac/buildspec.yml)
it uses, to scan and spin up the sample CFTs
in the iac (Infrastructure-as-Code) folder.*

#### Lab 19.1.2

Fix the errors in the CFTs that caused the scan to 'Fail'

- Ensure that there are no policies with * as the action
- Ensure that the "Encrypted" key exists and is set to "true"
  for any EBS resources that may be created
- Ensure that all Security Groups have Egress rules included explicitly

Start the project using [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/codebuild/index.html)
and get the logs (Logs are stored in CloudWatch)

Note the warnings in the CFTs in the iac folder. These may not fail the build,
but are still best practices that need to be fixed/implemented.

### Retrospective 19.1

#### Question: cfn_nag - Warning vs Fail

Can the Warning W2 be used to break/stop the build?
