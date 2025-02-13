import os, json
from datetime import datetime, timedelta, time as datetime_time
from src.parameters import *
from src.azure_storage_file_datalake import azure_config
from src.oci_object_storage import oci_config

class utilities_config:
    # Compare lists
    def compare_lists(source_list, target_list):
        try:
            count_equal = 0
            count_update = 0
            count_new = 0
            data_list = []
            entry = None
            run_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
            run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for s in source_list:
                if (s.content_length > 0):
                    if (len(target_list)>0):
                        for t in target_list:
                            if (s.name == t.name):
                                if (s.content_length == t.size):                                
                                    entry = {'source_name': s.name, 'source_size': s.content_length, 'targe_name': t.name, 'targe_size': t.size, 'start_date':run_date, 'end_date':run_date, 'run_time':'0:00:00', 'run_date':run_date, 'run_id':run_id, 'status':'equal' }                 
                                    count_equal = count_equal + 1
                                    break
                                else:
                                    entry = {'source_name': s.name, 'source_size': s.content_length, 'targe_name': t.name, 'targe_size': t.size, 'start_date':'0000-00-00 00:00:00', 'end_date':'0000-00-00 00:00:00', 'run_time':'0:00:00', 'run_date':run_date, 'run_id':run_id, 'status':'update' }
                                    count_update = count_update + 1
                                    break
                            else:
                                entry = {'source_name': s.name, 'source_size': s.content_length, 'targe_name': t.name, 'targe_size': t.size, 'start_date':'0000-00-00 00:00:00', 'end_date':'0000-00-00 00:00:00', 'run_time':'0:00:00', 'run_date':run_date, 'run_id':run_id, 'status':'new' }
                    else:
                        entry = {'source_name': s.name, 'source_size': s.content_length, 'targe_name': s.name, 'targe_size': s.content_length, 'start_date':'0000-00-00 00:00:00', 'end_date':'0000-00-00 00:00:00', 'run_time':'0:00:00', 'run_date':run_date, 'run_id':run_id, 'status':'new' }
                        
                    data_list.append(entry)

            count_new = len(data_list) - (count_equal + count_update)

            print('  Object(s) detected: ' + str(len(data_list)))
            print('               equal: ' + str(count_equal))
            print('              update: ' + str(count_update))
            print('                 new: ' + str(count_new))
            print('  Compare lists...[Succeded]\n')

            return data_list
        
        except Exception as e:
            print(e)

    # Copy objects from Azure to OCI
    def copy_objects_from_azure_to_oci(data_list, service_client):
        
        i = 0

        for d in data_list:
            if (d['status'] != 'equal'):
                start = datetime.now()
                d['start_date'] = start.strftime('%Y-%m-%d %H:%M:%S')

                print('# Download file (' + d['source_name'] + ')...')
                obj_bytes = azure_config.download_file(d['source_name'], service_client)
                                
                print('  Upload object (' + d['source_name'] + ')...')
                object_name = d['source_name']
                oci_config.upload_object(par_utl_log_bucket_name, object_name, obj_bytes)
                
                end = datetime.now()
                d['end_date'] = end.strftime('%Y-%m-%d %H:%M:%S')
                
                d['run_time'] = str(utilities_config.time_diff(start, end)).split(".")[0]

                i = i + 1

        print('  Updated object(s): ' + str(i))

        print('  Copy object(s) from Azure to OCI...[Succeded]\n')

        return data_list 

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

    def time_diff(start, end):        
        if isinstance(start, datetime_time): # convert to datetime
            assert isinstance(end, datetime_time)
            start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
        if start <= end: # e.g., 10:33:26-11:15:49
            return end - start
        else: # end < start e.g., 23:55:00-00:25:00
            end += timedelta(1) # +day
            assert end > start
            return end - start