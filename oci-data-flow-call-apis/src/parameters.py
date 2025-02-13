import oci

# [Parameter:api_eda] Food Database API
par_api_eda_app_id               = '300e527a'
par_api_eda_app_key              = '7f2b394c11f5708beab5370716719e43'

# [Parameter:oci_obj] OCI Object Storage
par_oci_obj_bucket_name            = 'madhacks-target'
# The profile parameter (ociProfileName) 'LOCAL' or 'DATAFLOW' in OCI
par_oci_obj_ociProfileName         = 'LOCAL'
par_oci_obj_ociConfigFilePath      = ('/opt/dataflow/python/lib/python3.6/site-packages/src/.oci/config' if par_oci_obj_ociProfileName=='DATAFLOW' else 'src/.oci/config')
par_oci_obj_config                 = oci.config.from_file(par_oci_obj_ociConfigFilePath, par_oci_obj_ociProfileName)
par_oci_obj_object_storage_client  = oci.object_storage.ObjectStorageClient(par_oci_obj_config)
par_oci_obj_namespace_name         = par_oci_obj_object_storage_client.get_namespace().data

# [Parameter:oci_adb] OCI Autonomous Database
par_oci_adb_lib_dir                = ('/opt/dataflow/python/lib/python3.6/site-packages/src/.oci/instantclient_19_11' if par_oci_obj_ociProfileName=='DATAFLOW' else 'src/.oci/instantclient_19_11')
par_oci_adb_user                   = 'admin'
par_oci_adb_password               = 'DemoDataSync2021@'
par_oci_adb_dsn                    = 'demoadw_high'
par_oci_adb_credential             = 'OBJ_STORE_CRED'
par_oci_adb_region                 = 'us-ashburn-1'

# [Parameter:utl_json] Copy Json
par_utl_json_object_name            = 'edamam_food_database_api.json'
par_utl_json_directory              = 'files/api/' + par_utl_json_object_name

# [Parameter:utl_dow] Download Object
par_utl_dow_directory              = 'files/img/'