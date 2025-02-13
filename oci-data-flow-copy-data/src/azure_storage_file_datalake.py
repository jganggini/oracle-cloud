from src.parameters import *
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential

class azure_config:
    # Connect to the account
    def initialize_storage_account():        
        try:
            if par_az_oau:
                credential = ClientSecretCredential(par_az_oau_tenant_id, par_az_oau_client_id, par_az_oau_client_secret)

                service_client = DataLakeServiceClient(account_url='{}://{}.dfs.core.windows.net'.format(
                    'https', par_az_sac_storage_account_name), credential=credential)
                print('  Connect to OAUT...[Succeded]\n')
            else : 
                service_client = DataLakeServiceClient(account_url='{}://{}.dfs.core.windows.net'.format(
                    'https', par_az_sac_storage_account_name), credential=par_az_key_storage_account_key)
                print('  Connect to KEY...[Succeded]\n')

            return service_client

        except Exception as e:
            print(e)

    # List the contents of the directory
    def list_directory_contents(service_client):
        try:
            file_system_client = service_client.get_file_system_client(file_system=par_az_sac_file_system)
            
            paths_list = file_system_client.get_paths(path=par_az_sac_path)

            print('  List the contents [AZURE]...[Succeded]\n')

            return paths_list

        except Exception as e:
            print(e)

    # Download file
    def download_file(name, service_client):
        try:
            file_system_client = service_client.get_file_system_client(file_system=par_az_sac_file_system)

            directory_client = file_system_client.get_directory_client(par_az_sac_file_directory)

            file_client = directory_client.get_file_client("./" + name)

            download = file_client.download_file()

            obj_bytes = download.readall()

            print('  Download file (' + name + ')...[Succeded]\n')

            return obj_bytes

        except Exception as e:
            print(e)