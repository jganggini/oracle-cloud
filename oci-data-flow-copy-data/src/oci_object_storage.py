import json
from src.parameters import *

class oci_config:
    # List the contents of the directory
    def list_directory_contents():
        try:
            object_list = par_oci_obj_object_storage_client.list_objects(par_oci_obj_namespace_name, par_oci_obj_bucket_name, fields='name,timeCreated,size')
            
            paths_list = object_list.data.objects

            print('  List the contents [OCI]...[Succeded]\n')

            return paths_list

        except Exception as e:
            print(e)

    # Upload file to OCI
    def upload_object(bucket_name, object_name, obj_bytes):
        try:
            par_oci_obj_object_storage_client.put_object(namespace_name=par_oci_obj_namespace_name,bucket_name=bucket_name, object_name=object_name, put_object_body=obj_bytes)

            print('  Upload object (' + object_name + ')...[Succeded]\n')

        except Exception as e:
            print(e)

    # Gets the metadata and body of an object
    def download_object(bucket_name, object_name):
        try:
            get_object_response = par_oci_obj_object_storage_client.get_object(namespace_name=par_oci_obj_namespace_name,bucket_name=bucket_name, object_name=object_name)

            print('  Download object (' + object_name + ')...[Succeded]\n')

            return get_object_response

        except Exception as e:
            print('  Download object (' + object_name + ') not exists...[Warning]\n')
            
            return e
            
   # Add entry to json object in OCI 
    def add_entry_to_json_object_in_oci(bucket_name, object_name, data_list):
        try:
            print('# Download object (' + object_name + ')...')
            obj = oci_config.download_object(bucket_name, object_name)
            
            if (obj.status == 404):                
                print('  Upload object (' + object_name + ')...')
                obj_bytes = json.dumps(data_list)
                oci_config.upload_object(bucket_name, object_name, obj_bytes)
            else:
                print('  Edit object (' + object_name + ')...')
                
                obj_bytes = obj.data.content

                # Decode UTF-8 bytes to Unicode, and convert single quotes 
                # to double quotes to make it valid JSON
                obj_str = obj_bytes.decode('utf8').replace("'", '"')

                # Load the JSON to a Python list & dump it back out as formatted JSON
                obj_list = json.loads(obj_str)

                for d in data_list:
                    obj_list.append(d)
                
                print('  Edit object (' + object_name + ')...[Succeded]\n')

                print('  Upload object (' + object_name + ')...')
                obj_bytes = json.dumps(obj_list)
                oci_config.upload_object(bucket_name, object_name, obj_bytes)

            print('  Add entry to json object (' + object_name + ')...[Succeded]\n')

        except Exception as e:
            print(e)