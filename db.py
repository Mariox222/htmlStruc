
import pymongo
from pprint import pprint
import time
import json

# w5dNm9Lj4zrhOJ8

class Experimenter:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.connect()
    
    def connect(self):
        self.client = pymongo.MongoClient(self.conn_str)
        self.db = self.client.websecradar
        print("connected")
    
    def getHashPairs(self, hash_pairs_n=10, sleepInterval=5, batch_size=10, filename='hash_pairs.json', docs_from=0, docs_to=None):
        print("getting pairs")
        url_col = self.db.crawled_data_urls_v0

        hash_pairs = []
        skipped = 0
        total_document_count = 0
        req_count = batch_size

        count = 1956352 # hardkodirano jer dinamičko određivanje predugo traje
        print("document count is: {}".format(count))

        assert (count >= docs_from)
        if docs_to:
            assert (count >= docs_to)
        else:
            docs_to = count
        
        for document in url_col.find(batch_size=batch_size)[docs_from:docs_to]:
            
            total_document_count += 1

            last_hash = ""
            second_last_hash = ""
            for check in reversed(document['checks']):
                if check['timestamp'] == document['last_check']:
                    last_hash = check['hash']
                if check['hash'] != last_hash and last_hash != "":
                    second_last_hash = check['hash']
                    break
            
            if (second_last_hash == ""):
                skipped += 1
            else:
                if last_hash == None:
                    print("one site's last check doesn't have a hash")
                else:
                    hash_pairs.append({'second_last_hash': second_last_hash, 'last_hash': last_hash})

            req_count = req_count - 1

            if req_count <= 0:
                req_count = batch_size

                if len(hash_pairs) >= hash_pairs_n:
                    break
                else:
                    
                    print (" --- skipped {} documents".format(skipped))
                    print ("hash_pairs: {}".format(len(hash_pairs)))
                    print ("total documents viewed: " + str(total_document_count))
                    print("sleep {} seconds\n".format(sleepInterval))
                    time.sleep(sleepInterval)

                    skipped = 0
                    continue
        
        print("Got {} hash pairs".format(len(hash_pairs)))
        print ("writing hash pairs to '{}'".format(filename))
        pprint (hash_pairs)

        written = 0
        with open(filename, 'w') as f:
            json.dump(hash_pairs, f)
            print(" --- writing complete")
            written = 1
        
        if not written:
            print("write failed")

    def getDocs(self):
        pass
    

def main():
    batch_size = 10
    sleepInterval = 5
    num_of_hash_pairs_to_get = 10
    docs_from = 20
    docs_to = 60

    json_filename = 'hash_pairs.json'
    conn_str = "mongodb://rouser:MiLaBiLaFiLa123@127.0.0.1:27017/websecradar?authSource=websecradar"

    exp = Experimenter(conn_str)
    exp.getHashPairs(batch_size=batch_size, hash_pairs_n=num_of_hash_pairs_to_get, sleepInterval=sleepInterval, filename=json_filename, docs_from=docs_from, docs_to=docs_to)


    print ("done")



if __name__ == "__main__":
    main()



