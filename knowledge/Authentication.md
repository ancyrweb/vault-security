**Authentication** identifies the user, distinguishing one user and their permissions from another. Mistakes mean malicious logins. What an identified user may then do is [[Authorization]].

## Methods
- **Username and password**: the username uniquely identifies the user, the password is evidence *they* created the account, and e-mail confirmation is evidence they *own* the address. See [[Hashing]] for storing passwords.
- [[Multi-Factor Authentication]]: combines several kinds of evidence, such as something you know and something you have
- **API keys and tokens**: most APIs rely on these rather than sessions or cookies. JSON Web Tokens (JWTs) are the most used.
- [[OpenID Connect]]: a standard for robust authentication, typically based on JWTs
- **Machine to machine**: Mutual [[Transport Layer Security|TLS]] and IP allow lists

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
