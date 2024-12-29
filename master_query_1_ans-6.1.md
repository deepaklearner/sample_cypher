Apologies for missing that! Let's add the `neo4j_operations.py` file, which will include the business logic to handle interactions with Neo4j. This file will have operations for connecting to Neo4j, querying the database, and performing any necessary operations such as creating nodes, updating data, or running queries.

Here's how we can structure `neo4j_operations.py` for both version 1 and version 2:

### 1. **Neo4j Operations for Version 1 (`neo4j_operations.py`)**

The following code demonstrates how to interact with the Neo4j database using the `neo4j` Python driver, run queries, and return the results. The structure remains the same in `v1` and `v2`, but as your use cases evolve, you can customize the operations.

#### `api/v1/neo4j_operations.py`

```python
# api/v1/neo4j_operations.py

from neo4j import GraphDatabase
from typing import List, Dict
import logging
import os
from src.utils.retrieve_azure_creds import ReadSecretsFromKeyVault

class Neo4jDatabase:
    def __init__(self, config_path: str):
        # Initialize the configuration path
        self.config_path = config_path
        self.uri, self.username, self.password = self.get_neo4j_credentials()
        self.driver = None

    def get_neo4j_credentials(self):
        # Fetch credentials from Azure Key Vault using the ReadSecretsFromKeyVault
        creds_reader = ReadSecretsFromKeyVault(self.config_path)
        azure_creds = creds_reader.read_secret_from_keyvault()
        
        # Extract Neo4j credentials
        neo4j_creds = azure_creds["NE04"]
        uri = neo4j_creds["HostURI"]
        username = neo4j_creds["Username"]
        password = neo4j_creds["Password"]
        return uri, username, password

    def connect(self):
        """Establish connection to Neo4j database."""
        if not self.driver:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        return self.driver

    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()

    def execute_query(self, query: str, parameters: Dict = {}) -> List[Dict]:
        """Execute a read query in Neo4j."""
        session = self.connect().session()
        result = session.run(query, parameters)
        return [record.data() for record in result]

    def create_node(self, node_label: str, properties: Dict) -> str:
        """Create a node in Neo4j."""
        session = self.connect().session()
        query = f"CREATE (n:{node_label} {{ {', '.join([f'{k}: ${k}' for k in properties])} }}) RETURN n"
        result = session.run(query, properties)
        session.close()
        return "Node created successfully" if result else "Failed to create node"

    def get_nodes(self, label: str) -> List[Dict]:
        """Retrieve all nodes with the given label."""
        query = f"MATCH (n:{label}) RETURN n"
        return self.execute_query(query)

    def get_relationships(self, label_1: str, label_2: str, rel_type: str) -> List[Dict]:
        """Retrieve relationships between two node labels."""
        query = f"""
        MATCH (n:{label_1})-[r:{rel_type}]-(m:{label_2})
        RETURN n, r, m
        """
        return self.execute_query(query)

# Example usage of the Neo4jDatabase class
def fetch_neo4j_data():
    neo4j_db = Neo4jDatabase(config_path="/path/to/config/config.yaml")
    nodes = neo4j_db.get_nodes("Person")
    neo4j_db.close()
    return nodes

```

### Key Points:
- **Initialization**: The `Neo4jDatabase` class is initialized with the path to the config file, which allows fetching credentials from Azure Key Vault.
- **Connection**: The `connect` method establishes a connection to the Neo4j database using the credentials.
- **CRUD Operations**: 
  - `execute_query`: A helper method to execute a general Cypher query (read-only).
  - `create_node`: A method to create a new node with properties.
  - `get_nodes`: A method to fetch all nodes for a given label.
  - `get_relationships`: A method to fetch relationships between two labels.
- **Closing the Connection**: Always ensure you close the Neo4j connection when done.

### 2. **Neo4j Operations for Version 2 (`neo4j_operations.py`)**

In version 2, you may have additional features or updates to the existing logic. For example, in version 2, you could add more advanced queries or modify the node structure.

#### `api/v2/neo4j_operations.py`

```python
# api/v2/neo4j_operations.py

from neo4j import GraphDatabase
from typing import List, Dict
import logging
from src.utils.retrieve_azure_creds import ReadSecretsFromKeyVault

class Neo4jDatabaseV2:
    def __init__(self, config_path: str):
        # Initialize the configuration path for v2
        self.config_path = config_path
        self.uri, self.username, self.password = self.get_neo4j_credentials()
        self.driver = None

    def get_neo4j_credentials(self):
        # Fetch credentials from Azure Key Vault
        creds_reader = ReadSecretsFromKeyVault(self.config_path)
        azure_creds = creds_reader.read_secret_from_keyvault()
        
        # Extract Neo4j credentials
        neo4j_creds = azure_creds["NE04"]
        uri = neo4j_creds["HostURI"]
        username = neo4j_creds["Username"]
        password = neo4j_creds["Password"]
        return uri, username, password

    def connect(self):
        """Establish connection to Neo4j database."""
        if not self.driver:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        return self.driver

    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()

    def execute_query(self, query: str, parameters: Dict = {}) -> List[Dict]:
        """Execute a read query in Neo4j."""
        session = self.connect().session()
        result = session.run(query, parameters)
        return [record.data() for record in result]

    def create_node(self, node_label: str, properties: Dict) -> str:
        """Create a node in Neo4j."""
        session = self.connect().session()
        query = f"CREATE (n:{node_label} {{ {', '.join([f'{k}: ${k}' for k in properties])} }}) RETURN n"
        result = session.run(query, properties)
        session.close()
        return "Node created successfully" if result else "Failed to create node"

    def get_nodes(self, label: str) -> List[Dict]:
        """Retrieve all nodes with the given label."""
        query = f"MATCH (n:{label}) RETURN n"
        return self.execute_query(query)

    def get_relationships(self, label_1: str, label_2: str, rel_type: str) -> List[Dict]:
        """Retrieve relationships between two node labels."""
        query = f"""
        MATCH (n:{label_1})-[r:{rel_type}]-(m:{label_2})
        RETURN n, r, m
        """
        return self.execute_query(query)

    def update_node_property(self, label: str, node_id: str, property_key: str, new_value: str) -> str:
        """Update a property on an existing node."""
        query = f"""
        MATCH (n:{label} {{id: $node_id}})
        SET n.{property_key} = $new_value
        RETURN n
        """
        params = {"node_id": node_id, "new_value": new_value}
        result = self.execute_query(query, params)
        return "Node updated successfully" if result else "Failed to update node"

# Example usage of the Neo4jDatabaseV2 class
def fetch_neo4j_data_v2():
    neo4j_db = Neo4jDatabaseV2(config_path="/path/to/config/config.yaml")
    nodes = neo4j_db.get_nodes("Employee")
    neo4j_db.close()
    return nodes
```

### Key Points for Version 2:
- **Additional Features**: In version 2, we introduced an `update_node_property` method that updates a property on an existing node, which could be a feature not present in version 1.
- **Refined Structure**: The core logic is similar, but the code is ready for any additional operations in future versions.

### Connecting Neo4j Operations in FastAPI

In both versions of the API, you would import and use the respective `Neo4jDatabase` or `Neo4jDatabaseV2` classes inside your `main.py` endpoints to interact with Neo4j. Here's an example of how you might use it:

```python
# api/v1/main.py (example usage of Neo4jDatabase)
from fastapi import APIRouter
from api.v1.neo4j_operations import Neo4jDatabase

router = APIRouter()

@router.get("/v1/neo4j-nodes")
async def get_neo4j_nodes():
    neo4j_db = Neo4jDatabase(config_path="/path/to/config/config.yaml")
    nodes = neo4j_db.get_nodes("Person")
    neo4j_db.close()
    return nodes
```

### Conclusion:
- The `neo4j_operations.py` file includes key functionality for interacting with the Neo4j database.
- You have `Neo4jDatabase` for version 1 and `Neo4jDatabaseV2` for version 2, allowing for future extensions and versioning.
- The business logic is modular and reusable across the FastAPI app.

With these additions, you can now perform Neo4j operations such as creating nodes, querying nodes, and managing relationships directly within your FastAPI endpoints.