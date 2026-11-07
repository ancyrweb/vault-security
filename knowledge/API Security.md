**API security** is approached as risk management: every defense should lower the likelihood or the impact of an attack (see [[Security Risk]]).

## Design
- [[Security Principles]]: the general principles applied here
- [[Attack Surface Minimization]]: fewer endpoints, less data returned
- [[Threat Modeling]]: user input, supply chain, caching and logs are the main API threats

## Threats
- [[Input Validation]]: never trust user input, the main source of attacks on APIs
- [[Supply Chain Attack]]: compromise through dependencies, IDE and cloud environments

## Secrets and private data
- **Secrets**: don't store them in code. Private repositories aren't safe either.
- [[Cryptography]]: hashing, encryption and signatures
- [[Transport Layer Security|TLS]]: every API call should use it
- [[Database Encryption]]: protecting sensitive data once stored

## Access
- [[Authentication]]: identifying the user, with API keys and tokens as the usual mechanism

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
