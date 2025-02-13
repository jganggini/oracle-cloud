from src.parameters import *
from src.oci_autonomous_database import oci_autonomous_database
from src.oci_object_storage import oci_object_storage
from src.api_edamam import api_edamam
from src.utilities import utilities_config

def main():
    try:        
        print('# List contents of column {upc_ean_plu} of table {madhacks_upc} [OCI-AD]...')        
        oci_autonomous_database.Client()
        upc_list = oci_autonomous_database.list_table_values('madhacks_upc', 'upc_ean_plu')
        
        print('# List the contents [EDAMAM-API]...')
        food_database_list = api_edamam.list_food_database_api(upc_list)
        
        if(par_oci_obj_ociProfileName == 'LOCAL'):
            print('# Add entry to json object (LOCAL)...')
            utilities_config.add_entry_to_json_object_in_local(par_utl_json_directory, food_database_list)
        
        print('# Add entry to json object (OCI)...')
        oci_object_storage.add_entry_to_json_object_in_oci(par_oci_obj_bucket_name, par_utl_json_directory, food_database_list)
        
        print('# Truncate table {madhack_json_edamam} [OCI-AD]...')
        oci_autonomous_database.truncate_table('madhack_json_edamam')

        print('# Copy json collection to table {madhack_json_edamam} [OCI-AD]...')
        oci_autonomous_database.copy_collection_json('madhack_json_edamam', par_utl_json_directory)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    # create Spark context with Spark configuration
    main() 