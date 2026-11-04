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
	