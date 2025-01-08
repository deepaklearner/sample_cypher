teach me about ldap3
Server


LDAP (Lightweight Directory Access Protocol) is a protocol used for accessing and managing directory services, like user and group information, typically used in enterprise environments. `ldap3` is a Python library that allows for easy interaction with LDAP servers. 

To interact with an LDAP server, you need to create an instance of the `Server` class in the `ldap3` library. This instance represents the LDAP server and is the starting point for any connection, bind operation, or query you wish to make.

### 1. Installation
You can install `ldap3` via pip:
```bash
pip install ldap3
```

### 2. Basics of LDAP3 Server

The `Server` class in `ldap3` is used to represent an LDAP server and can be used for setting up connections to it. The server can be used either for direct connections or for handling more complex scenarios like connection pooling and load balancing.

### 3. `Server` Class: Key Parameters

The `Server` class has a few key parameters when initializing a connection:

- **`host`**: The hostname or IP address of the LDAP server.
- **`port`**: The port to connect to, usually 389 for non-secure connections or 636 for secure connections (LDAPS).
- **`use_ssl`**: A boolean flag indicating if the connection should be over SSL/TLS.
- **`get_info`**: Used to specify which server information to retrieve. Options include `ALL`, `SERVER`, `SCHEMA`, `NONE`, etc.
- **`timeout`**: A time limit for the connection to establish.

### Example: Creating a Server Object

```python
from ldap3 import Server

# Creating a Server object
server = Server('ldap://example.com', port=389, get_info='ALL')

# You can also use SSL if necessary:
# server = Server('ldaps://example.com', port=636, use_ssl=True, get_info='ALL')
```

### 4. Connection to the Server

After creating a `Server` object, you can create a connection to the server using the `Connection` class. 

```python
from ldap3 import Connection

# Create a connection to the server
conn = Connection(server, user='cn=admin,dc=example,dc=com', password='password')

# Open the connection
conn.bind()
```

### 5. Common Operations Using LDAP3

Once connected to the server, you can perform several operations such as:

- **Search**: You can search for entries in the directory.
- **Add**: You can add new entries.
- **Modify**: You can modify existing entries.
- **Delete**: You can delete entries.

#### Searching Entries

The search operation allows you to query the LDAP directory for specific entries.

```python
# Search for all users in the 'ou=users,dc=example,dc=com' organizational unit
conn.search('ou=users,dc=example,dc=com', '(objectClass=person)')

# Print the results
for entry in conn.entries:
    print(entry)
```

#### Adding an Entry

You can add entries to the LDAP directory.

```python
# Add an entry to the directory
entry_dn = 'uid=john.doe,ou=users,dc=example,dc=com'
attributes = {
    'objectClass': ['inetOrgPerson'],
    'cn': 'John Doe',
    'sn': 'Doe',
    'uid': 'john.doe',
    'userPassword': 'password123'
}

conn.add(entry_dn, attributes=attributes)
```

#### Modifying an Entry

Modify an existing entry with the `modify` method.

```python
# Modify an entry (e.g., change the last name)
conn.modify('uid=john.doe,ou=users,dc=example,dc=com', {'sn': [(MODIFY_REPLACE, ['NewLastName'])]})
```

#### Deleting an Entry

You can delete an entry using the `delete` method.

```python
conn.delete('uid=john.doe,ou=users,dc=example,dc=com')
```

### 6. Handling Server Information

When creating a `Server` object, the `get_info` parameter controls the retrieval of information from the LDAP server. The `ALL` option retrieves all available information (such as supported features and schema). If you just need basic information, you can use `SERVER`.

Example:

```python
from ldap3 import Server

# Get detailed server info
server = Server('ldap://example.com', get_info='ALL')
print(server.info)

# Get basic server info
server = Server('ldap://example.com', get_info='SERVER')
print(server.info)
```

### 7. Authentication and Security

LDAP servers often require authentication (bind) before performing operations. You can authenticate using different methods, such as:

- **Simple Bind**: Provides a username and password for authentication.
- **SASL Bind**: A more complex authentication method, often used in secure environments.

Example of simple bind:
```python
conn = Connection(server, user='cn=admin,dc=example,dc=com', password='password')
conn.bind()
```

For secure connections, `use_ssl=True` enables SSL encryption, and you can also specify a certificate if needed.

```python
server = Server('ldaps://example.com', use_ssl=True)
```

### 8. Error Handling

`ldap3` raises exceptions for various error cases. Some common exceptions include:

- **`LDAPBindError`**: Raised if binding (authentication) fails.
- **`LDAPSocketOpenError`**: Raised if the connection cannot be established.
- **`LDAPException`**: Base class for all exceptions in the library.

Example:

```python
from ldap3 import LDAPBindError, LDAPSocketOpenError

try:
    conn.bind()
except LDAPBindError:
    print("Failed to bind, check username and password.")
except LDAPSocketOpenError:
    print("Failed to connect to the server.")
```

### 9. Connection Pooling

In larger systems with many connections to an LDAP server, it's often beneficial to use connection pooling for efficiency. `ldap3` supports connection pooling, which allows for reusing established connections.

Example:

```python
from ldap3 import Server, Connection, Pool

# Create a connection pool
server = Server('ldap://example.com')
pool = Pool(server, user='cn=admin,dc=example,dc=com', password='password', size=5)

# Use pooled connections
conn = pool.get_connection()
conn.bind()
```

### Conclusion

The `Server` class in `ldap3` is a critical component for interacting with an LDAP server. It is used to specify server details and to configure and manage connections. From there, you can perform various operations such as adding, modifying, searching, and deleting LDAP entries.

Would you like to dive deeper into any specific area or explore more advanced LDAP functionality?