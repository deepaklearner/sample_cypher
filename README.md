I need you to design and implement a reusable LDAP connector library in Python, based on my existing codebase.

Requirements:
- Create a modular "connector framework" similar to JDBC in Java.
- There should be a single public-facing LDAP connector class (gateway).
- Internally, it should manage multiple connection objects (one per domain/config).
- Connection credentials/config must be centralized and not passed every time.
- Only runtime parameters like search filters, attributes, and queries should be passed by the caller.
- Follow object-oriented design:
  - Public methods for external use
  - Private/internal methods for connection handling
- The connector should support multiple LDAP-based systems (e.g., Active Directory domains).
- It should be extensible so we can add other connectors later (e.g., Neo4j, databases).
- Organize code into a "connectors" module/folder.
- Avoid duplicating connection logic across jobs—this should replace per-job connection utilities.
- Ensure thread-safe or independent connection handling for parallel job execution.
- Use a modern Python LDAP library (prefer ldap3 unless my codebase already uses something else).
- Include example usage showing how a job would call this connector with just a search filter.

Also:
- Analyze my existing code and refactor any repeated LDAP connection logic into this shared connector.
- Preserve backward compatibility where possible.

Output:
- Clean class design
- Code implementation
- Example usage
- Suggestions for improvements or scalability