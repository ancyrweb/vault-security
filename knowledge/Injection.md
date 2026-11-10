**Injection** is getting attacker-supplied input interpreted as code or commands by the system or by other users. It exploits APIs that trust [[Input Validation|user input]].

## Types
- **Cross-Site Scripting (XSS)**: injected JavaScript is executed by other users.
- **SQL injection**: running custom SQL on the database.
- **NoSQL injection**: the same idea against NoSQL databases, with different syntax.
- **Server-Side Request Forgery (SSRF)**: the attacker tricks the server into making unintended requests to internal resources, local systems (`localhost`, `127.0.0.1`) or cloud metadata endpoints.

## Defenses
Layer several, per [[Defense in Depth]]:
- **Web Application Firewall (WAF)**: inspects incoming requests and tries to detect malicious content.
- **Ingress filtering**: allow in only specific, expected traffic.
- [[Authentication]]: limits who can reach the vulnerable code at all.
- [[Input Validation]] and input sanitization.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
