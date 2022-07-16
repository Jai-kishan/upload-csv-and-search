from search_data.settings import db

class DbHelper:
    
    def feed_data_inot_db(self,data):
        ##! bulk insert
        result = db.product.insert_many(data)
        return result
    
    def get_all_product(self):
        ##! getting the list of all recods
        result = list(db.product.find({},{"sku_code":1}))
        return result, len(result)
    
    def get_search_data(self, data,skip,limit):
        ##! using the 'or' and 'regex' searching the text data from the db
        query = {
             '$or': [
                # {"sku_code": {"$regex": data, "$options":"i"}},
                {"product_name": {"$regex": data, "$options":"i"}},
                {"product_description": {"$regex": data, "$options": "i"}}   
                      ]
        }
        result = list(db.product.find(query))
        count = (len(result))
        if count > 0:
            return result[skip:limit], count
        return 0, 0