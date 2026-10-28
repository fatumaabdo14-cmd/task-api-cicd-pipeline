# Task API CI/CD Pipeline

A serverless task API (AWS Lambda + DynamoDB) delivered through a GitHub Actions pipeline that deploys every pull request to its own CloudFormation test stack and removes it on merge.

## Architecture

```
Pull request ──► GitHub Actions ──► CloudFormation stack: pr-test-stack-<PR number>
                                      ├─ Lambda function (Python 3.12)
                                      ├─ IAM execution role
                                      └─ DynamoDB table (on-demand)
PR merged    ──► GitHub Actions ──► delete-stack
```

The function writes to and reads from the DynamoDB table, returning the task list as JSON. The table name is injected as an environment variable, so the same code runs unchanged in every stack.

## Repository

| Path | Purpose |
|---|---|
| `.github/workflows/cfn-validate-pr.yml` | Per-PR deploy, PR comment, cleanup on merge |
| `cloudformation/lambda.yml` | Lambda function, execution role and DynamoDB table |
| `lambda/lambda_function.py` | Function source for local testing |

## Key decisions

- **Isolated stacks per PR.** Function and table names are suffixed with the stack name, so concurrent pull requests never share data or resources.
- **Pay-per-request DynamoDB.** Test stacks cost nothing while idle.
- **Comment only on open PRs.** The PR comment step is skipped on the `closed` event so merged PRs aren't spammed.

## Setup

1. Add `AWS_ACCESS_KEY_ID2026` and `AWS_SECRET_ACCESS_KEY2026` as repository secrets.
2. Open a pull request against `main`.

## Next steps

- Scope the execution role from `AmazonDynamoDBFullAccess` down to `GetItem`/`PutItem`/`Scan` on this table only.
- Put API Gateway in front of the function for a public HTTP endpoint.
- Move to GitHub OIDC instead of long-lived access keys.

---

**Fatuma Abdo** · Cloud Engineer · [LinkedIn](https://www.linkedin.com/in/fatuma-abdo-3b729a3a4)
