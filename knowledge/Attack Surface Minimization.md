---
aliases: [Attack Surface Reduction]
---
**Attack surface minimization** reduces [[Security Risk|risk]] by shrinking what an attacker can reach: less code and less data, less risk. The extreme case, no API at all, is zero risk. In practice:

- Reduce the number of endpoints.
- Reduce the amount of data the API returns.
- Remove old databases that are no longer used.
- Remove unused functionality from libraries.
- Remove forgotten or undocumented endpoints and features: attackers abuse these "shadow functions".

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
