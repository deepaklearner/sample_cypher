From the base DN, you should derive the domain (e.g., parsing it appropriately). Also, the ID attribute should not default to something like `employeeId`—instead, you need to explicitly define which attribute acts as the primary key.

You should not have a “start button”; instead, define a “start key.” This key determines where or how the process begins and should be included in the YAML configuration.

That said, these are the only additional details that need to go into the YAML file. Beyond this, the YAML should remain minimal. Most of the information should not be defined here but instead be passed dynamically from the job when it initiates or creates the connection.

As mentioned earlier, in scenarios where multiple jobs (e.g., account–entitlement relationships) share 50+ similar connections, we should maintain a common configuration layer. This file should not reside in the connector. The connector should only contain connector-specific logic, such as SSL configuration and validation rules.

There is no need for a dedicated YAML file just to create a connector.

The main goal is to avoid repeatedly importing the L3 library for every component. Instead, all connections should be initialized centrally and exposed as reusable connection objects.

We can configure this so that a connection object (e.g., named for ADH) is created once and passed around. The connector should read required details directly from the key vault.

For use cases like AD email sync, we should not configure all connection details within that module. The purpose of the custom library is to avoid repeatedly passing full configurations. Instead, we pass minimal identifiers (e.g., something like `ad_<identifier>`), and the library resolves the rest.

In the key vault:

* Store all connection-specific details such as connection strings and passwords.
* Do not rely on upstream or legacy wallets—define a new, structured key vault approach.

We should also define a consistent naming convention for keys (e.g., prefixes like `ldap` or similar patterns), followed by domain-specific identifiers. However, for environments like corporate domains (e.g., multiple domain variations), we still need to standardize how this mapping will work.

In the configuration:

* Do not store raw usernames or passwords.
* Only include references (pointers) to the key vault entries that contain the actual values.

