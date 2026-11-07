# Understanding API Security Fundamentals

API Security is all about risk
**Risk** = **Likelihood** (times) **impact**. We have to understand how likely an attack is and the ultimate impact if the attack is successful.

We add defenses that either decrease likelihood, impact, or both.

**Common Vulnerability Scoring System** : calculates the exact risk score for your vulnerabilities.

**Attack Surface Minimization** : No API = Zero Risk but it's a little bit extreme. 
Reduce number of endpoints.
Reduce amount of data out of the API.
Get rid of old database that is no longer used.
Remove functionalities from libraries.
Less Code & Less Data = Less Risk

**Security as an egg** : the system is inside the egg, attacks comes from outside.
If an attacker breaches the edge, it can attack the inside any way they please.

Defensive layers reduce risk.
There's always residual risk
- Incorrectly implemented defenses
- Circumvented defenses
- Completely new attacks
We must assume every defense will fail.
We create multiple defenses for each risk.

# Applying secure design principles to API

**Thread Modeling** : understing likely attacks and use that information to direct defensive efforts.

Approaches :
- **User Input**
	- **Never Trust User Input**
	- Main source of attacks against API
	- Solution
		- Expect incoming data to be manipulated
		- Validate all input
		- Add thought to that validation
- **Supply Chain Attacks**
	- **Never trust the supply chain**
	- Chain of digital components
		- IDE
		- Libraries
		- Cloud environments
	- Solution
		- Remove unneeded dependencies
		- Remove unneeded extensions in IDE
		- Run dependency checks
		- Harden Environments : ensure users and developers use only the tools they need
		- Set user permissions carefully
- **Cache Attacks**
	- Tricking the system into caching data it shouldn't like API Keys
	- **Solution**
		- Don't cache sensitive informations
- **Logs**
	- Storing sensitive informations in logs
	- **Solution**
		- Don't log sensitive information in logs
		- Put thoughts in logging

# Managing API secrets and private data

- Where not to store secrets :
	- Don't store secrets in code
	- Private repositories aren't safe either
- Using Cryptography effectively
	- Hashing
		- One-way encryption
		- The result represent the original data
		- It doesn't contain it so we can't rewind
		- Returns a digest
		- Slight change in input result in large change in output
		- Useful for data you never need to see again like passwords
		- Nowadays, Argon2id is preferred (2026)
	- Symmetric Encryption
		- Two-way encryption
		- The same key both encrypts and decrypts
		- Encrypt the data with the key -> get ciphertext
		- Decrypt ciphertext with the key to get data
	- Asymmetric Encryption
		- Two-way encryption
		- Two keys
			- Public key : encrypts the data
			- Private key : decrypts the data
	- Every API call should use TLS
		- Latest version
		- Test TLS connection with `SSL Labs`test
- Using Signatures
	- Take a file (like a PDF) and sign it to get a digest
	- The digest prove the file hasn't been altered
	- Next : keep the digest itself safe
		- Encrypt it using the private key to get a signed PDF
		- Decrypt it using the public key
- Database Encryption
	- Sensitive information in database should be protected
		- Using symmetric encryption, manually
		- Con : can't search encrypted data
	- Encryption at rest
		- Databases stored as files
		- These files can be encrypted at rest
		- It happens transparently 

# Implementing API Authentication mechanisms

- Authentication
	- Is about identifying the user
	- Distinguish a user and their permissions from another
	- Mistakes mean malicious logins
- Methods
	- Username / Password based authentication
		- Username uniquely identify the user
		- Password is evidence *they* created the account
		- E-mail confirmation is evidence they *own* the e-mail address
	- Multi-Factor Authentication
		- Combine multiple informations
			- Something you know
				- Password
			- Something you have
				- Digital Security Key
				- Mobile phone
				- One-time PINs
			- Something you are
				- Fingerprint
				- Face scans
			- Where you are
	- Tokens and sessions
		- Most APIs don't use sessions
		- Most APIs don't rely on cookies either
		- They rely on API keys and tokens
		- JSON Web Tokens are the most used
	- OpenID connect
		- Standard for robust authentication
		- Typically based on JWTs
		- Complicated
		- Uses long-lived refresh token and short-lived access-token
	- Machine to machine authentication
		- Uses Mutual TLS
		- IP allow list