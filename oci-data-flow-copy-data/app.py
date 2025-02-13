from src.parameters import *
from src.azure_storage_file_datalake import azure_config
from src.oci_object_storage import oci_config
from src.utilities import utilities_config

def main():
    try:
        print('# Connect to the account in Azure...')
        azure_service_client = azure_config.initialize_storage_account()
        
        print('# List the contents [Azure]...')
        azure_paths_list = azure_config.list_directory_contents(azure_service_client)
               
        print('# List the contents [OCI]...')
        oci_paths_list = oci_config.list_directory_contents()
        
        print('# Compare lists...')
        azure_paths_list = list(azure_paths_list)
        oci_paths_list = list(oci_paths_list)
        compare_list = utilities_config.compare_lists(azure_paths_list, oci_paths_list)
        
        print("# Copy object(s) from Azure to OCI...")
        copy_list = utilities_config.copy_objects_from_azure_to_oci(compare_list, azure_service_client)
        
        print("# Add entry to json object (log)...")
        (oci_config.add_entry_to_json_object_in_oci(par_oci_obj_bucket_name, par_utl_log_object_name, copy_list) if par_oci_obj_ociProfileName=='DATAFLOW' else utilities_config.add_entry_to_json_object_in_local(par_utl_log_object_name, copy_list))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # create Spark context with Spark configuration
    main()
    