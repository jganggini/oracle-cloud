import json
import cx_Oracle
from src.parameters import *

class oci_autonomous_database:
    # Client
    def Client():
        try:
            cx_Oracle.init_oracle_client(lib_dir=par_oci_adb_lib_dir)

            print('  Client [OCI-AD]...[Succeded]')

        except Exception as e:
            print(e)
            
    # List table values
    def list_table_values(table_name, columns):
        try:
            connection = cx_Oracle.connect(user=par_oci_adb_user, password=par_oci_adb_password, dsn=par_oci_adb_dsn)

            cursor = connection.cursor()

            row_list = []

            for row in cursor.execute('select ' + columns + ' from ' + table_name):
                row_list.append(row[0])
            
            print('  List contents of column {' + columns + '} of table {' + table_name + '} [OCI-AD]...[Succeded]\n')

            return row_list

        except Exception as e:
            print(e)

    # Truncate Table
    def truncate_table(table_name):
        try:
            connection = cx_Oracle.connect(user=par_oci_adb_user, password=par_oci_adb_password, dsn=par_oci_adb_dsn)

            cursor = connection.cursor()
            
            query = 'TRUNCATE TABLE '+ table_name

            print('  Truncate table (' + table_name + ')...[Succeded]\n')

            cursor.execute(query)

        except Exception as e:
            print(e)

    # Truncate Table
    def copy_collection_json(table_name, object_directory):
        try:
            connection = cx_Oracle.connect(user=par_oci_adb_user, password=par_oci_adb_password, dsn=par_oci_adb_dsn)

            cursor = connection.cursor()
            
            query = """
            BEGIN DBMS_CLOUD.COPY_COLLECTION(    
                collection_name => '""" + table_name + """',
                credential_name => '""" + par_oci_adb_credential + """',
                file_uri_list =>
                'https://objectstorage.""" + par_oci_adb_region + """.oraclecloud.com/n/""" + par_oci_obj_namespace_name + """/b/""" + par_oci_obj_bucket_name + """/o/""" + object_directory + """',
                format =>
                JSON_OBJECT('unpackarrays' value 'true') );
            END;
            """
            
            print('  Copy json collection to table (' + table_name + ')...[Succeded]\n')

            cursor.execute(query)

        except Exception as e:
            print(e)