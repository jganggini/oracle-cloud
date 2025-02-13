import requests
import urllib3
from datetime import datetime
from src.parameters import *
from src.utilities import utilities_config
from src.oci_object_storage import oci_object_storage

class api_edamam:
    # List the contents of the directory
    def list_food_database_api(upc_list):
        try:
            # https://developer.edamam.com/admin/applications/1409622171147
            # https://developer.edamam.com/food-database-api-docs

            food_database_list = []
            entry = None
            run_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for upc in upc_list:

                payload = {
                    "app_id"    : par_api_eda_app_id,
                    "app_key"   : par_api_eda_app_key,
                    "upc"       : upc}

                response = requests.get("https://api.edamam.com/api/food-database/v2/parser", params=payload)

                j = response.json()
                
                entry = { 'upc_ean_plu': upc, 'text': str(j['text']) }

                for hints in j['hints']:
                    for key_food, value_food in hints['food'].items():
                        
                        if key_food == 'label': 
                            entry['food_' + key_food] = value_food

                        elif key_food == 'image': 
                            entry['food_' + key_food] = value_food
                            
                            print('  Download object (' + par_oci_obj_ociProfileName + ')...')
                            object_name = par_utl_dow_directory + upc + '.jpg'
                            if(par_oci_obj_ociProfileName =='LOCAL'):
                                utilities_config.download_object_in_local(value_food, object_name)

                            print('  Upload object (' + object_name + ')...')
                            obj_bytes = urllib3.PoolManager().request('GET', value_food).data
                            oci_object_storage.upload_object(par_oci_obj_bucket_name, object_name, obj_bytes)

                        elif key_food == 'nutrients': 
                            for key_nutrients, value_nutrients in value_food.items():
                                entry['food_nutrients_' + key_nutrients] = value_nutrients
                        
                        elif key_food == "servingSizes":
                            for servingSizes in value_food:
                                for key_servingSizes, value_servingSizes in servingSizes.items():
                                    entry['food_servingSizes_' + key_servingSizes] = value_servingSizes

                        elif key_food == "qualified":
                            for qualified in value_food:
                                for key_qualified, value_qualified in qualified.items():
                                    entry['food_qualified_' + key_qualified] = value_qualified

                        else: 
                            entry['food_' + key_food] = value_food
                    
                    for measures in hints['measures']:
                        for key_measures, value_measures in measures.items():
                            if key_measures != 'qualified': 
                                entry['measures_' + key_measures] = value_measures
            
                    entry['run_date'] = run_date
                    entry['run_id'] = run_id

                food_database_list.append(entry)

            print('  List the contents [EDAMAM-API]...[Succeded]\n')

            return food_database_list

        except Exception as e:
            print(e)