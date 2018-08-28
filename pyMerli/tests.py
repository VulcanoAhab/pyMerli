import json
import yaml
import time
import unittest
from search import Request
from config import FromFile
from kafka import KafkaProducer,KafkaConsumer
from kafka.errors import KafkaError


class SearchRequest(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        #kafka send job test
        self.remote_config=FromFile("config_dev.yaml").settings

        #search test
        self.merli=Request("tv box", "MLB", 1000, 0)
        self.item_keys=["id",
                        "site_id",
                        "title",
                        "seller",
                        "price",
                        "currency_id",
                        "available_quantity",
                        "sold_quantity",
                        "buying_mode",
                        "listing_type_id",
                        "stop_time",
                        "condition",
                        "permalink",
                        "thumbnail",
                        "accepts_mercadopago",
                        "installments",
                        "address",
                        "shipping",
                        "seller_address",
                        "attributes",
                        "original_price",
                        "category_id",
                        "official_store_id",
                        "catalog_product_id",
                        "reviews",
                        "tags",
                        "request",
                        "description",
                        "questions"]

    def test_offers(self):
        """
        """
        #items get
        items=list(self.merli.offers(limit=50))
        self.assertTrue(len(items))
        #item request & morphology
        item=items[0]
        self.assertEqual(item["request"]["item_count"], 50)
        self.assertEqual(item["request"]["page_count"], 0)
        self.assertEqual(set(item.keys()), set(self.item_keys))

    def test_kafka(self):
        """
        """
        #send job
        producer = KafkaProducer(
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
            bootstrap_servers=["localhost:9092"])
        print("[+] Sending job: {}".format(
            json.dumps(self.remote_config, indent=3)))
        future=producer.send("merli-jobs", self.remote_config)
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            log.exception()
            pass
        # Successful result returns assigned partition and offset
        print("[+] Sent job:\n")
        print ("\tTopic:",record_metadata.topic)
        print ("\tPartition:",record_metadata.partition)
        print ("\tOffset:",record_metadata.offset)

        #subscribe to results
        consumer = KafkaConsumer("merli-results",
                bootstrap_servers=["localhost:9092"])
        print("[+] Waiting results from Merli job:{}".format(
                                    self.remote_config["name"]))
        for msg in consumer:
            print("[+] Received: {}".format(msg.value.decode()))
            print(("."*75)+"\n")


    if __name__ == "__main__":
        unittest.main()
