---
aliases: [Access Control]
---
**Authorization** decides what an authenticated user is allowed to do. It is a separate check from [[Authentication]]: knowing who the user is doesn't say which objects or actions they may access.

## Models
- **Role-based model (RBAC)**: each user has a role, and the role determines what they can do.
- **Access control matrix**: a table grants rights per user and per subject, as tuples `[user, subject, right]`.

## Separate admin API
Split administrative functions into their own API, separate from the regular one, so it can carry much stricter restrictions such as an IP allow list.

## Vulnerabilities
- [[Broken Object Level Authorization]] (BOLA/IDOR): the user is authenticated, but access to the specific object isn't checked.
- **Broken Object Property Level Authorization (BOPLA)**: access to the object as a whole is checked, but granular checks on its individual properties (fields) are missing.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
