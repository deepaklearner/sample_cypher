iam_create_graph = IAMGraphCreation(self.database_config)

try:
    with iam_create_graph:
        batch_counter = 1
        concat_warning_report_df = pd.DataFrame()
        concat_error_report_df = pd.DataFrame()
        entitlements_neo4j = pd.DataFrame()
        updated_entitlements = pd.DataFrame()

        while True:
            logging.info(f"Processing entitlements batch {batch_counter}")
            logging.info(f"Fetch batch data from entitlement master")

            # Step 1: Read entitlements in batches from entitlement master
            entitlements_edw = entitlement_ingestion.fetch_batch_data_from_entitlement_master(
                feature_name, entitlements_query_param, chunksize, offset
            )
            logging.info(f"length={len(entitlements_edw)} | \n{entitlements_edw.to_string()}")

            # Step 1a: Fetch the entitlements data from Neo4j
            if len(entitlements_edw) > 0:
                logging.info("Fetch the entitlements data from Neo4j")
                entitlements_list = entitlements_edw[['entitlementName', 'targetSystem']].drop_duplicates().to_dict('records')
                entitlements_neo4j = iam_create_graph.fetch_entitlement_data_from_graph(entitlements_list)
                logging.info(f"entitlements_neo4j:\n{entitlements_neo4j.to_string()}")

                # Step 1b: New entitlements
                if len(entitlements_neo4j) > 0:
                    new_entitlements = entitlements_edw[
                        ~entitlements_edw['concat_attr_entitlements1'].isin(entitlements_neo4j['concat_attr_entitlements1'])
                    ]
                else:
                    new_entitlements = entitlements_edw
                logging.info(f"new_entitlements:\n{new_entitlements.to_string()}")

                # Step 1c: Create the missing entitlement nodes in Neo4j
                if len(new_entitlements) > 0:
                    logging.info("Creating new Entitlement nodes")
                    iam_create_graph.create_entitlement_nodes(new_entitlements, feature_name)

                # Step 1d: Update existing entitlements
                if len(entitlements_neo4j) > 0:
                    logging.info("Updating existing Entitlement nodes")
                    merged_temp_df = pd.merge(
                        entitlements_edw,
                        entitlements_neo4j[['concat_attr_entitlements1', 'concat_attr_entitlements2']],
                        on='concat_attr_entitlements1',
                        how='inner',
                        suffixes=('_edw', '_neo4j')
                    )
                    logging.info(f"merged_temp_df:\n{merged_temp_df.to_string()}")

                    updated_entitlements = merged_temp_df[
                        merged_temp_df['concat_attr_entitlements2_edw'] != merged_temp_df['concat_attr_entitlements2_neo4j']
                    ]
                    logging.info(f"updated_entitlements:\n{updated_entitlements.to_string()}")
                    iam_create_graph.update_entitlement_nodes(updated_entitlements, feature_name)

                # Step 2: Enrich new and updated entitlements with owner details
                delta_entitlement_nodes = pd.concat([new_entitlements, updated_entitlements], ignore_index=True)
                if len(delta_entitlement_nodes):
                    logging.info("Fetch related data from eservice_data")
                    keys = tuple(
                        delta_entitlement_nodes[['entitlementName', 'targetSystem']]
                        .drop_duplicates()
                        .itertuples(index=False, name=None)
                    )
                    placeholders = ','.join(['%s'] * len(keys))
                    eservice_data_df = entitlement_ingestion.fetch_data_from_eservice(
                        feature_name, eservice_query_param, placeholders, keys
                    )
                    logging.info(f"eservice_data_df:\n{eservice_data_df.to_string()}")

                    # Step 3: Join enriched data with entitlement master
                    edw_entitlements = delta_entitlement_nodes.merge(
                        eservice_data_df, on=['entitlementName', 'targetSystem'], how='left'
                    )
                    logging.info("Validating owners in graph db and creating warning/error report")

                    # Step 4: Generate reports
                    owner_columns = ['owner1', 'owner2', 'owner3']
                    all_owner_ids = pd.unique(edw_entitlements[owner_columns].values.ravel())
                    all_owner_ids = {x for x in all_owner_ids if not (isinstance(x, float) and math.isnan(x))}

                    logging.info(f"all_owner_ids: {all_owner_ids}")
                    owners_with_status = iam_create_graph.validate_owners_status(all_owner_ids)
                    logging.info(f"owners_with_status:\n{owners_with_status.to_string()}")

                    if owners_with_status.empty:
                        logging.info("No users found in Neo4j for this batch")
                        inactive_owners_df = pd.DataFrame()
                        missing_owners = all_owner_ids
                    else:
                        inactive_owners_df = owners_with_status[owners_with_status['Reason'] != 'Active']
                        missing_owners = all_owner_ids - set(owners_with_status['OwnerID'])

                    missing_owners_df = pd.DataFrame({'OwnerID': list(missing_owners), 'Reason': 'Owner missing in Neo4j db'})
                    logging.info(f"warning report:\n{inactive_owners_df.to_string()}")
                    logging.info(f"error report:\n{missing_owners_df.to_string()}")

                    concat_warning_report_df = pd.concat([concat_warning_report_df, inactive_owners_df], ignore_index=True)
                    concat_error_report_df = pd.concat([concat_error_report_df, missing_owners_df], ignore_index=True)

                    # Step 5: Assign and update entitlement owners
                    logging.info("Assign and update entitlement owners")
                    iam_create_graph.assign_n_update_entitlement_owners(edw_entitlements, feature_name)

                offset += chunksize
                batch_counter += 1
            else:
                logging.info(f"No records fetched from SQL query - [BatchSize: {offset}-{offset+chunksize}]")
                break

        # Write the final reports
        self.write_report_to_csv(
            configstream, self.report_file_location, concat_warning_report_df, concat_error_report_df
        )

except Exception as e:
    logging.error(
        f"Error in Processing Batch: {batch_counter} - Offset: {offset} "
        f"- Debug <Class: IAMDataExecutor | Method: create_graph_for_entitlements()> | {e}"
    )
finally:
    entitlement_ingestion.close_connections()

return True
