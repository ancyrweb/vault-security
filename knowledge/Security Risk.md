---
aliases: [Risk, Residual Risk]
---
**Risk** = **likelihood** × **impact**: how likely an attack is, times the damage if it succeeds. Every defense should decrease likelihood, impact, or both.

- [[Common Vulnerability Scoring System|CVSS]] rates vulnerability severity (exploitability and impact), not risk: how likely an attack is in your environment has to be assessed separately.
- [[Attack Surface Minimization]] lowers risk by removing what can be attacked.

## Residual risk
Some risk always remains, because defenses can be:
- implemented incorrectly
- circumvented
- defeated by completely new attacks

That's why [[Defense in Depth]] assumes every defense will fail.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
