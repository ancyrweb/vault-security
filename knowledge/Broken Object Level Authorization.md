---
aliases: [BOLA, Insecure Direct Object Reference, IDOR]
---
**Broken Object Level Authorization (BOLA)**, also called **Insecure Direct Object Reference (IDOR)**, happens when an application properly checks the user's [[Authentication|authentication]] but not whether they are allowed to access a specific object or resource. It is a failure of [[Authorization]].

## Mitigation
- **Always scope queries** to everything the request implies, even when it seems redundant, so a user never reaches resources they shouldn't. For `foobar.com/organization/123/invoice/456`, the SQL query filters on organization ID `123` *and* invoice ID `456`, not just the invoice ID. This is [[Defense in Depth]] at the data layer.
- Use GUIDs as identifiers instead of guessable (e.g. sequential) IDs.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
