import oci

# [Parameter:az_sac] Storage Account
par_az_sac_storage_account_name    = 'sourcedemo'
par_az_sac_file_system             = 'parquetfiles'
par_az_sac_path                    = ''
par_az_sac_file_directory          = '.'

# [Parameter:az_oau] OAUTH
par_az_oau                         = False
par_az_oau_tenant_id               = '********-****-****-****-***********'
par_az_oau_client_id               = '********-****-****-****-***********'
par_az_oau_client_secret           = '********-**********.******'

# [Parameter:az_key] KEY
par_az_key_storage_account_key     = '3MKEQ7dBY4e6xeIsw4uEBXR9gG1QuZa2T64uoNyyktINq...'

# [Parameter:oci_obj] OCI Object Storage
par_oci_obj_bucket_name            = 'target-azure'
# The profile parameter (ociProfileName) 'LOCAL' or 'DATAFLOW' in OCI
par_oci_obj_ociProfileName         = 'DATAFLOW'
par_oci_obj_ociConfigFilePath      = ('/opt/dataflow/python/lib/python3.6/site-packages/src/.oci/config' if par_oci_obj_ociProfileName=='DATAFLOW' else './src/.oci/config')
par_oci_obj_config                 = oci.config.from_file(par_oci_obj_ociConfigFilePath, par_oci_obj_ociProfileName)
par_oci_obj_object_storage_client  = oci.object_storage.ObjectStorageClient(par_oci_obj_config)
par_oci_obj_namespace_name         = par_oci_obj_object_storage_client.get_namespace().data

# [Parameter:utl_log] Control
par_utl_log_bucket_name            = 'target-azure'
par_utl_log_object_name            = ('log/log_dataflow_app_migration.json' if par_oci_obj_ociProfileName=='DATAFLOW' else './log_dataflow_app_migration.json')