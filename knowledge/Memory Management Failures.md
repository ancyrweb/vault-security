**Memory management failures** are bugs in how a program allocates and uses memory, which unexpected or oversized input can trigger.

- **Buffer overflow**: user input exceeds the allocated memory and overwrites adjacent memory.
- **Integer overflow**: a numeric value exceeds its type's maximum and wraps around to zero.
- **Memory exhaustion**: allocated memory isn't deallocated, so the process eventually runs out.

## Sources
- [[courses/pluralsight/api-security-best-practices/Notes|API Security Best Practices]] (course, Pluralsight)
