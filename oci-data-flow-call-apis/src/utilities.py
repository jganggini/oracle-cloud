import os, json, requests
from datetime import datetime, timedelta, time as datetime_time
from src.parameters import *

class utilities_config:

    # Add entry to json object in LOCAL
    def add_entry_to_json_object_in_local(object_name, data_list):
        try:            
            if os.path.isfile(object_name):
                print ('  Local file exists...')
                with open(object_name, 'r+') as file:
                    obj_list = json.load(file)
                    
                    for d in data_list:
                        obj_list.append(d)

                    file.seek(0)
                    json.dump(obj_list, file)
            else:                
                print ('  Local file not exist...')
                with open(object_name, 'w') as file:
                    json.dump(data_list, file)

            print('  Add entry to json object (' + object_name + ')...[Succeded]\n')

        except Exception as e:
            print(e)

    # Download Object in LOCAL
    def download_object_in_local(object_url, object_name):
        try:            
            object = requests.get(object_url).content
            with open(object_name, 'wb') as handler:
                handler.write(object)

            print('  Download objecto in local (' + object_name + ')...[Succeded]')

        except Exception as e:
            print(e)
