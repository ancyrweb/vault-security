**Threat modeling** identifies the attacks a system is likely to face, so defensive effort goes where it matters.

## Main API threats
- **User input**: the main source of attacks against APIs. See [[Input Validation]].
- **Supply chain**: every component used to build and run the system is a way in. See [[Supply Chain Attack]].
- **Caching**: tricking the system into caching data it shouldn't, such as API keys. Don't cache sensitive information.
- **Logs**: sensitive information ends up stored in logs. Don't log it, and decide deliberately what gets logged.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
