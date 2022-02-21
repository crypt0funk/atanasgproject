import config
import query_twitter
# Load  dataset
data = query_twitter.dataframe
# Connect to MongoDB
client =  config.local_client
mydb = client["Twitter"]
collection = mydb["Dataset"]
data.reset_index(inplace=True)
data_dict = data.to_dict("records")
# Insert collection
collection.insert_many(data_dict)