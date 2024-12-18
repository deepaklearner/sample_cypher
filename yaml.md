supervisor_hierarchy_ProjConfig:
  log_location: /opt/cvs/deepak/logs/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy
  notification_log_location: /opt/cvs/deepak/logs/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy/notification
  techops_log_location: /opt/cvs/logs/deepak/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy/notification/techops
  timeout_duration: 14400
  main_log_history_days: 30
  error_log_history_days: 30
  stat_log_history_days: 30
  venv_location: /opt/cvs/deepak/venv/bin/activate
  dev_keyvaulturi: kv-corpneo4j0101
  uat_east_keyvaulturi: kv-corpneo4j0601
  uat_central_keyvaulturi: kv-corpneo4j0602
  prod_east_keyvaulturi: kv-corpneo4j0701
  prod_central_keyvaulturi: kv-corpneo4j0702
  notification_config: /opt/cvs/deepak/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/config/supervisor_hierarchy_notification.yaml
  batch_size: 5000

supervisor_hierarchy_report_ProjConfig:
  log_location: /opt/cvs/deepak/logs/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy
  notification_log_location: /opt/cvs/deepak/logs/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy/notification
  techops_log_location: /opt/cvs/logs/deepak/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/populate_supervisor_hierarchy/notification/techops
  timeout_duration: 14400
  main_log_history_days: 30
  error_log_history_days: 30
  stat_log_history_days: 30
  venv_location: /opt/cvs/deepak/venv/bin/activate
  dev_keyvaulturi: kv-corpneo4j0101
  uat_east_keyvaulturi: kv-corpneo4j0601
  uat_central_keyvaulturi: kv-corpneo4j0602
  prod_east_keyvaulturi: kv-corpneo4j0701
  prod_central_keyvaulturi: kv-corpneo4j0702
  notification_config: /opt/cvs/deepak/Neo4J_Inbound_dev/pipeline_routines/supervisor_hierarchy/config/supervisor_hierarchy_notification.yaml
  batch_size: 5000

