from product.response_helper import ResponseHelper
from product.db_helper import DbHelper

import json, time
import pandas as pd
from bson import ObjectId
from product.response_helper import ResponseHelper

Response = ResponseHelper()
DbHelper = DbHelper()

class OperationHelper:
    def validate_request_body(self, request_data, mandatory_key):
        try:
            """
            This method validates request and parmas data
            """

            message = ""

            #####! check request body validation #####
            for count, i in enumerate(mandatory_key):
                if not i in request_data.keys():
                    message = f"{i} key is missing in the body"
                    return message
                elif not request_data.get(i):
                    message = f"{i} should not be empty in the body"
                    return message
            return message
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            finalResponse = {
                "message": message,
                "data": [],
                "result": [],
            }
            return Response.get_status_500(finalResponse)
        
    def upload_csv_data(self, data):
        try:
            file_nmae, extention = data.FILES['file_url'].name.split('.')
            
            ##! if file extension not csv
            if extention != 'csv':
                return Response.get_status_400("This is not a csv file format")
            
            ##! readnig the csv file
            df = pd.read_csv(data.FILES['file_url'])
            df.fillna('')
            
            ##! getting the list of columns name
            column_name = list(df.columns)

            mandatory_columns = [
                'sku_code',
                'product_name',
                'product_description'
            ]
            
            ##! check which columns should be needed in the csv file
            for i, col in enumerate(mandatory_columns):
                if not col in column_name:
                    return Response.get_status_404(f"{col} is not exists in csv data")
            
            ##! check if we have extra columns or not 
            if len(column_name) > 3:
                return Response.get_status_400(f"csv has only this -> {mandatory_columns} column data")

            product_list, count = DbHelper.get_all_product()

            if count == 0 :
                print("if")
                res = df.to_dict(orient='records')

            else:
                print("else")
                csv_sku_code = list(df['sku_code'])
                db_sku_code_list = [product['sku_code'] for product in product_list]

                ##! inserting unique record in db
                product_not_exists_in_db   = list(set(csv_sku_code).difference(db_sku_code_list))
                print("product_not_exists_in_db",product_not_exists_in_db)
                
                if not product_not_exists_in_db:
                    return Response.get_status_200("Getting duplicate records")
                
                product_df = df.loc[df["sku_code"].isin(product_not_exists_in_db)]
                
                ##! converting df data in to dict
                res = product_df.to_dict(orient='records')
            

            data_insert_res = DbHelper.feed_data_inot_db(res)     
            final_res = {
                "acknowledged":data_insert_res.acknowledged,
                "insertedIds": [str(i)for i in data_insert_res.inserted_ids]
            }
            return Response.get_status_200(final_res)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            finalResponse = {
                "message": message,
                "data": [],
                "result": [],
            }
            return Response.get_status_500(finalResponse)
        
    def get_search_data(self,data,skip,limit):
        try:
            search_text = data.get("search_data")
            search_data_res, count = DbHelper.get_search_data(search_text,skip,limit)
            
            if not search_data_res:
                return Response.get_status_404()
            
            ##! using pandas just converting the ObjectIds into string  
            df = pd.DataFrame(search_data_res)
            df['_id'] = df['_id'].apply(lambda x: str(x))
            search_res = df.to_dict(orient='records')
            
            final_res = {
                "data": search_res,
                "count": count
            }
            return Response.get_status_200(final_res)
        
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            finalResponse = {
                "message": message,
                "data": [],
                "result": [],
            }
            return Response.get_status_500(finalResponse)