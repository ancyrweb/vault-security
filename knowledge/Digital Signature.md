---
aliases: [Signature]
---
A **digital signature** proves that a file, such as a PDF, hasn't been altered.

## How it works
1. Produce a [[Hashing|digest]] of the file. The digest proves the file hasn't changed, as long as the digest itself stays safe.
2. Protect the digest by encrypting it with the private key, which gives the signed file.
3. Decrypt it with the public key to verify. See [[Asymmetric Encryption]].

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
