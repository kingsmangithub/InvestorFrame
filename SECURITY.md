# Security Policy

## Supported Versions

InvestorFrame is under active development. At this stage, security fixes are most likely to be applied to the latest version on the default branch.

---

## Reporting a Vulnerability

If you discover a security issue, please do **not** open a public GitHub issue with sensitive details.

Instead, report the issue privately to the project maintainer through an appropriate private contact channel.

When reporting a vulnerability, include:

- a clear description of the issue
- affected area or file
- reproduction steps
- impact assessment
- any suggested remediation if available

Please avoid sharing:

- secrets
- API keys
- tokens
- internal credentials
- private URLs
- personally identifiable information

---

## Scope of Security Concerns

Relevant security topics may include:

- accidental exposure of API keys or secrets
- unsafe handling of environment variables
- insecure default configuration
- weak auth patterns in future hosted surfaces
- server-side request handling issues
- dependency vulnerabilities
- unsafe export or report rendering behavior
- insecure use of third-party integrations

---

## Secrets and Credentials

Never commit any of the following to the repository:

- `.env`
- API keys
- auth tokens
- cloud credentials
- webhook secrets
- private certificates
- database passwords

Use:

- `.env.example` for placeholders
- local environment variables for real secrets
- platform secret stores for deployments

If a secret is accidentally committed:

1. remove it from the codebase
2. rotate it immediately
3. invalidate the exposed credential
4. clean repository history if necessary

---

## Dependency Hygiene

Please keep dependencies:

- minimal
- current
- necessary

When adding dependencies:

- explain why they are needed
- prefer mature and well-maintained packages
- avoid unnecessary heavy integrations
- check for known security issues where possible

---

## Data Safety

InvestorFrame is a research product and may interact with:

- market data
- scenario outputs
- watchlists
- external APIs

Contributors should be careful not to introduce behavior that:

- leaks sensitive data
- exposes private config
- stores unnecessary user data
- mixes demo data with sensitive data
- overexposes internal diagnostics in API responses

---

## Secure Defaults

Contributors are encouraged to prefer:

- explicit configuration
- safe fallbacks
- least privilege
- minimal logging of sensitive context
- clear separation of public and private config

Avoid:

- printing secrets in logs
- returning stack traces to end users
- unsafe CORS defaults in production
- hardcoded credentials
- hidden external calls without disclosure

---

## Disclaimer

InvestorFrame is a research and decision-support system. It is not designed for handling brokerage credentials, trade execution permissions, or regulated financial account operations.

If future versions introduce hosted, authenticated, or user-specific functionality, the security model should be reviewed and expanded accordingly.
