import sys
from os import path
import time, datetime, json, requests, pymongo, pytz, redis
from threading import Timer, Thread, Event


class PneumoniaRec():
    cached_time: str = ""  # type: str

    @classmethod
    # -------------
    # Get UTC time
    # -------------
    def utcnow(self):
        return datetime.datetime.now(tz=pytz.utc)

    # -------------
    # Write to MGDB collection
    # -------------
    def mgdb_write(self):
        # UTC epoch time
        sec = time.mktime(time.gmtime())
        # url might be change, need to add validation function
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(sec * 1000)
        print(url)
        data = json.loads(requests.get(url=url).json()['data'])
        print(data)
        new_time = list(data.values())[0] # very bad practice need to change
        if new_time != self.cached_time:
            saved_file_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

            print (__main__.__file__)
            with open('~Downloads/data.txt', 'w') as outfile:
                json.dump(data, outfile)
                cached_time = new_time

        # time stamp handling
        time_stamp = self.utcnow().isoformat()[:19]
        # print("utcnow:", time_stamp)
        name_timed = "FY_{}".format(time_stamp)
        print("col_name", name_timed)

        # Create new tables with timestamps
        mycol = mydb[name_timed]
        print(mydb.list_collection_names())
        x = mycol.insert_one(data)


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(300):  # every 5 mins
            print("my thread")
            # calls

# Connection to redis
database = redis.StrictRedis(host='localhost', port=6379, db=0)
# render = web.template.render(os.path.join(main_path, 'templates'))

urls = (
	'/', 'index',
	'/page', 'page',
)


# Create MongoDB client and database
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
dbList = myClient.list_database_names()
mydb = myClient["pneumonia"]
print(myClient.list_database_names())

myFY = PneumoniaRec();
myFY.mgdb_write()


