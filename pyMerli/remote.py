"""
kafka servers samples
#  needs DRY  #
"""
import json
import time
import datetime
from search import Request
from persist import S3
from kafka import KafkaConsumer, KafkaProducer

class JobServer:
    """
    """
    _hosts=["localhost:9092",]

    @classmethod
    def _convert_time(cls, obj):
        """
        """
        if not isinstance(obj, datetime.datetime):return
        return obj.__str__()

    @classmethod
    def _convert_obj(cls, obj):
        """
        """
        return json.dumps(obj,
               default=cls._convert_time).encode("ascii")

    @classmethod
    def set_hosts(cls, value):
        """
        """
        cls._hosts=value

    @classmethod
    def process_job(cls, job):
        """
        """
        job=json.loads(job.value.decode())
        tuplesTasks=[
        (termValues["value"], country, country+category, termValues["offset"])
        for termDict in job["terms"]
        for termKey, termValues in termDict.items()
        for country in job["countries"]
        for category in job["categories"]]
        for tupleTask in tuplesTasks: yield tupleTask


    @classmethod
    def main(cls):
        """
        """
        producer = KafkaProducer(
            value_serializer=cls._convert_obj,
            bootstrap_servers=["localhost:9092"])
        consumer=KafkaConsumer("merli-jobs", bootstrap_servers=cls._hosts)
        print("[+] Waiting merli-jobs")
        for job in consumer:
            print("[+] Got job:", job)
            for task in cls.process_job(job):
                producer.send("merli-tasks", task)


class TaskServer:
    """
    """
    @classmethod
    def main(cls):
        """
        """
        producer = KafkaProducer(
            value_serializer=cls._convert_obj,
            bootstrap_servers=["localhost:9092"])
        consumer=KafkaConsumer("merli-tasks", bootstrap_servers=cls._hosts)
        print("[+] Waiting merli-tasks")
        for task in consumer:
            print("[+] Got task:", task)
            merli=Request(*json.loads(task.value.decode()))
            try:
                for offer in merli.offers():
                    producer.send("merli-offers", offer)
            except Exception as e:
                yield {"error":{
                        "message":str(e),
                        "timestamp":time.time(),
                        "job-tuple":tupleJob}}

class OfferS3Server:
    """
    """
    @classmethod
    def main(cls):
        """
        """
        producer = KafkaProducer(
            value_serializer=cls._convert_obj,
            bootstrap_servers=["localhost:9092"])
        consumer=KafkaConsumer("merli-offers", bootstrap_servers=cls._hosts)
        print("[+] Waiting merli-offers")
        for offer in consumer:
            print("[+] Got offer:", offer)
            merli=S3(*json.loads(offer.value.decode()))
            try:
                merli.save()
                producer.send("merli-logs", merli.postSave.message)
            except Exception as e:
                yield {"error":{
                        "message":str(e),
                        "timestamp":time.time(),
                        "job-tuple":tupleJob}}

class LogServer:
    """
    """
    @classmethod
    def main(cls):
        """
        """
        consumer=KafkaConsumer("merli-logs", bootstrap_servers=cls._hosts)
        print("[+] LogServer is on. Waiting messages...")
        for log in consumer:print("[>] {}".format(log.value.decode()))

## command line utils
if __name__ == "__main__":
    import argparse

    def get_server(server_type):
        """
        """
        servers={"logserver":LogServer,}
        server=server_type.lower()
        if server not in servers:
            msg="[-] Unkown server:{}".format(server)
            raise Exception(msg)
        return servers[server]

    parse=argparse.ArgumentParser(description="Fast Kakfa servers")
    parse.add_argument("--server", "-se", help="server type",
                                        default="logserver")
    parse.add_argument("--hosts", "-hs", help="hosts",
                                        default="localhost:9092,")
    args=parse.parse_args()
    merli=get_server(args.server)
    merli._hosts=args.hosts.split(",")
    merli.main()
