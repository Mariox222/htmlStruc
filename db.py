
from pathlib import Path
import pymongo
from pprint import pprint
import time
import json
import os
from htmlStruct import HtmlStruct


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
                if check['hash'] != last_hash and last_hash != "" and check['hash'] != None:
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
                if hash_pairs_n:
                    if len(hash_pairs) >= hash_pairs_n:
                        break
                    
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

    def getDocs(self, directory_name, hash_filename):
        print("getting docs")
        doc_col = self.db.crawled_data_pages_v0

        extra_backSlash = "/" if directory_name[-1] != "/" else ""
        directory = Path("./" + directory_name + extra_backSlash)

        if not directory.exists():
            raise "directory doesn't exist"
        

        count = 0
        with open(hash_filename, "r") as h:
            data_str = h.read()
            data = json.loads(data_str)
            for pair in data:
                print (" --- " + str(count) + " / " + str(len(data)))
                
                print("sleeping 2 sec")
                time.sleep(2)

                old_doc_doc = doc_col.find_one({"hash": pair['second_last_hash']})
                new_doc_doc = doc_col.find_one({"hash": pair['last_hash']})
                
                if not old_doc_doc or not new_doc_doc:
                    print("couldn't get documents")
                    continue
                
                old_doc = old_doc_doc['page']
                new_doc = new_doc_doc['page']

                newDir = directory / str(count)
                newDir.mkdir(exist_ok=True)

                old_doc_path = newDir / "old.html"
                with old_doc_path.open(mode="w", encoding="utf-8") as f:
                    f.write(old_doc)
                    print("old document written")
                
                new_doc_path = newDir / "new.html"
                with new_doc_path.open(mode="w", encoding="utf-8") as f:
                    f.write(new_doc)
                    print("new document written")
                
                count += 1



    
def makeHashFile():
    batch_size = 10
    sleepInterval = 5
    num_of_hash_pairs_to_get = None
    docs_from = 200
    docs_to = 1000

    json_filename = 'hash_pairs.json'
    conn_str = "mongodb://rouser:MiLaBiLaFiLa123@127.0.0.1:27017/websecradar?authSource=websecradar"

    exp = Experimenter(conn_str)
    exp.getHashPairs(batch_size=batch_size, hash_pairs_n=num_of_hash_pairs_to_get, sleepInterval=sleepInterval, filename=json_filename, docs_from=docs_from, docs_to=docs_to)

    print ("done")

def getDocs():
    directory_name = "documents"
    hash_filename = "hash_pairs.json"

    conn_str = "mongodb://rouser:MiLaBiLaFiLa123@127.0.0.1:27017/websecradar?authSource=websecradar"

    exp = Experimenter(conn_str)
    exp.getDocs(directory_name, hash_filename)

def checkInjectedStructures():
    
    directory_name = "documents"
    keepAttributes = False
    

    dir_path = Path(directory_name)

    docs_detected = list() # for printing out

    for subdir in dir_path.iterdir():
        
        old_str = ""
        new_str = ""
        
        if subdir.is_dir():

            for file in subdir.iterdir():
                if file.name == "old.html":
                    with file.open("r", encoding="utf-8") as f:
                        old_str = f.read()
                        print("old document readed")
                if file.name == "new.html":
                    with file.open("r", encoding="utf-8") as f:
                        new_str = f.read()
                        print ("new document readed")
        
            old_struc = HtmlStruct()
            new_struc = HtmlStruct()

            old_struc.parseHtml(old_str, keepAttributes=keepAttributes)
            new_struc.parseHtml(new_str, keepAttributes=keepAttributes)

            diff = old_struc.structDiff(new_struc)
            
            if not diff:
                print("changes beyond simple insertions")
                continue

            if len(diff) == 0:
                print("0 inserted structures")
                continue

            print(" --- found something")

            json_file = subdir / "inj_struc.json"
            
            l = list()

            for insertedStruct in diff:
                l.append(HtmlStruct.presentNodes(insertedStruct))

            with json_file.open("w", encoding="utf-8") as f:
                json.dump(l, f)
                print("writing complete")
                docs_detected.append(subdir.name)

    pprint(docs_detected)




def main():
    #makeHashFile()
    #getDocs()
    checkInjectedStructures()




if __name__ == "__main__":
    main()



