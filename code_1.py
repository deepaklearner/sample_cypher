def create_graph_for_Department_hierarchy(self, FeatureDF, feature_name="Department_hierarchy", batch_size=20000):
    if len(FeatureDF) > 0:
        query_depthierarchy = """
        UNWIND $rows AS row
        MERGE (dept:Department {departmentCode: row.currentcode})
        SET dept.department = row.currentdesc,
            dept.deptLevel = row.currentlvl
        WITH row, dept

        // Match existing relationships and delete them if necessary
        OPTIONAL MATCH (:User)-[r_has:MANAGES]->(dept)
        OPTIONAL MATCH (dept)-[r_report_to:REPORTS_TO]->(:Department)
        MATCH (globalid:GlobalIdentifierCounter)
        DELETE r_has, r_report_to

        // Create parent department relationship
        FOREACH (x IN CASE WHEN row.parentcode <> "DNE" THEN [1] END |
            MERGE (dept2:Department {departmentCode: row.parentcode})
            ON CREATE SET dept2.department = row.parentdesc,
                          dept2.deptLevel = row.parentlvl
            MERGE (dept)-[:REPORTS_TO]->(dept2)
        )

        // Create user-manager relationship
        FOREACH (x IN CASE WHEN row.current_manager <> "DNE" AND row.is_manager_exist_in_INT5043 = 'Y' THEN [1] END |
            MERGE (usr:User {employeeNumber: row.current_manager})
            ON CREATE SET usr.userProfileID = apoc.create.uuid(),
                          usr.globalID = toString(toInteger(globalid.lastAssignedCounterValue) + 1),
                          globalid.lastExecutionDate = localdatetime(),
                          globalid.lastAssignedCounterValue = toString(toInteger(globalid.lastAssignedCounterValue) + 1)
            MERGE (usr)-[:MANAGES]->(dept)
        )
        RETURN COUNT(*)
        """

        # Execute the query with Neo4j driver
        self.neo4j_session.run(query_depthierarchy, rows=FeatureDF.to_dict('records'))
