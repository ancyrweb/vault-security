---
aliases: [Hash, Digest]
---
**Hashing** is a one-way transformation that turns data into a **digest**. The digest represents the original data but doesn't contain it, so it can't be reversed.

- A slight change in the input results in a large change in the output.
- Useful for data you never need to see again, such as passwords.
- Argon2id is the preferred algorithm nowadays (2026).
- Digests are also the basis of a [[Digital Signature]].

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
