# -*- coding: utf-8 -*-

import json
import yaml
import time
import unittest
from kafka.errors import KafkaError
from kafka import KafkaProducer,KafkaConsumer

from config import FromFile
from api import Search
from objects import MerliOffer, MerliDescription, MerliQuestion
from extras.samples import RAW_OBJ, RAW_OBJ_DESC, RAW_OBJ_QUESTIONS


class SearchRequest(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        #kafka send job test
        self.remote_config=FromFile("pyMerli/extras/config_dev.yml").settings

        #search test • keyword, country_id, category_id - options dict
        self.search=Search("tvbox", "MLB", 1000, limit=25)
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
                        "questions",
                        ]

    def test_offers(self):
        """
        """
        #items get
        items=list(self.search.offers())[0]
        self.assertTrue(len(items))
        #item request & morphology
        item=items[0] #first result - item count 1
        self.assertEqual(item["metadata"]["item_count"], 1)
        self.assertEqual(item["metadata"]["page_count"], 0)
        #self.assertEqual(set(item.keys()), set(self.item_keys))

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

class Objects(unittest.TestCase):
    """
    """
    def setUp(self):
        """
        """
        self.offer=MerliOffer(RAW_OBJ)
        self.description=MerliDescription(RAW_OBJ_DESC)
        self.question=MerliQuestion(RAW_OBJ_QUESTIONS["questions"][0])
        self.offer_fields=[
            "id", "site_id", "title_cloud", "title", "seller_id",
            "seller", "price", "currency_id", "available_quantity",
            "sold_quantity", "buying_mode", "listing_type_id", "stop_time",
            "condition", "permalink", "thumbnail", "accepts_mercadopago",
            "installments_amount", "installments_quantity",
            "installments_currency", "installments", "location_state_id",
            "location_state_name", "location_city_id", "location_city_name",
            "address", "free_shipping", "shipping_mode", "shipping",
            "seller_country_name", "seller_country_id", "seller_city_name",
            "seller_city_id", "seller_state_name", "seller_state_id",
            "seller_zipcode", "seller_address", "brand", "item_condition",
            "model", "attributes", "original_price", "category_id",
            "official_store_id", "catalog_product_id", "reviews_total",
            "reviews_ratio", "reviews", "tags"
        ]
        self.description_fields=[
            "text", "plain_text_cloud", "mention_channels",
            "plain_text", "last_updated", "date_created", "snapshot"
        ]
        self.question_fields=[
            "date_created", "item_id", "seller_id", "status",
            "text_cloud", "text", "id", "answer"
        ]

    def test_offer(self):
        """
        """
        #object struct
        self.assertTrue(isinstance(self.offer, MerliOffer))
        self.assertEqual(self.offer_fields, self.offer._fields,
                              "[-] Object fields match fail")
        #some control fields
        self.assertEqual(self.offer.model, "PK1000", "[-] Fail model value")
        self.assertEqual(self.offer.title, "Amplificador Para Fone "\
                                "De Ouvido Pakrys Pk-1000 Power Play",
                                        "[-] Fail offer title match.")

    def test_description(self):
        """
        """

        self.assertEqual(self.description_fields,
                         self.description._fields,
                         "[-] Object fields match fail")

    def test_question(self):
        """
        """
        self.assertEqual(self.question_fields, self.question._fields,
                                      "[-] Object fields match fail")


if __name__ == "__main__":
    unittest.main()
