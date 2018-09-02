
import string
from datetime import datetime
from dateutil.parser import parse as date_parse

class Parser:
    """
    """
    _puncs=list(string.punctuation)
    _puncs_no
    _cloud=re.compile("([^{}\s]+[\S]+[^{}\s]+)|([\w\d]+)".format(
                                _puncs_no, _puncs_no,_puncs_no), re.M)
    @classmethod
    def world_list(cls, text_in):
        """
        """
        word_list=[]
        tuple_list=cls._cound.findall(text_in.lower())
        for tup in tuple_list:
            if not any(tup):continue
            if tup[0]:word_list.append(tup[0])
            else:
                if tup[1]:word_list.append(tup[1])
        return word_list

    def __init__(self, raw_obj):
        """
        """
        self.raw=raw_obj
        self._process()

    def _process(self):
        """
        """
        self._fields=[]
        self._fields_count=0
        for key,value in self._raw.items():
            try:
                parsed=getattr(self, key+"_parser")(value)
                setattr(self, key, parsed)
            except AttributeError:
                setattr(self, key, value.strip())
            self._fields.append(key)
            self._fields_count+=1

    @property
    def toDict(self):
        """
        """
        return self.__dict__


class MerliOffer(Parser):
    """
    """
    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def title_parser(self):
        """
        """
        self.title_cloud=self.word_cloud(self.raw["title"])
        return self.raw["title"]

    def attributes_parser(self):
        """
        """
        attrs=[]
        for attr in self.raw["attributes"]:
            key=attr["id"].lower()
            value=attr["value_name"]
            setattr(self, key, value)
            attrs.append(key)
        return "|".join(sorted(attrs))

    def site_id_parser(self):
        """
        """
        return self.raw["site_id"].lower()

    def currency_id_parser(self):
        """
        """
        return self.raw["currency_id"].lower()

    def stop_time_parser(self):
        """
        """
        return date_parse(self.raw["stop_time"])

    def reviews_parser(self):
        """
        """
        revis=self.raw["reviews"]
        self.reviews_total=revis["total"]
        self.reviews_ratio=revis["rating_average"]
        return self.reviews_ratio+"|"+self.reviews_total

    def installments_parser(self):
        """
        """
        insta=self.raw["installments"]
        self.installments_amount=insta["amount"]
        self.installments_quantity=insta["quantity"]
        self.installments_currency=insta["currency_id"].lower()
        insta["currency_id"]=self.installments_currency
        return (self.installments_currency+"|"
               +self.installments_amount+"|"
               +self.installments_quantity)

    def seller_parser(self):
        """
        """
        self.seller_id=self.raw["seller"]["id"]
        return self.raw["seller"]["id"]

    def address_parser(self):
        """
        """
        addr=self.raw["address"]
        self.location_state_id=addr["state_id"].lower()
        self.location_state_name=addr["state_name"].lower()
        self.location_city_id=ADDR["city_id"]
        self.location_city_name=addr["city_name"].lower()
        return self.location_city_name+"|"+self.location_state_name

    def shipping_parser(self):
        """
        """
        ships=self.raw["shipping"]
        self.free_shipping=ships["free_shipping"]
        self.shipping_mode=ships["mode"]
        return str(self.free_shipping)+|+self.shipping_mode

    def seller_address_parser(self):
        """
        """
        saddr=self.raw["seller_address"]
        self.seller_country_name=saddr["country"]["name"].lower()
        self.seller_country_id=saddr["country"]["id"].lower()
        self.seller_city_name=saddr["city"]["name"].lower()
        self.seller_city_id=saddr["city"]["id"].lower()
        self.seller_state_name=saddr["state"]["name"].lower()
        self.seller_state_id=saddr["state"]["id"].lower()
        self.seller_zipcode=saddr["zip_code"]
        return  (self.seller_country_id+"|"
                +self.seller_state_id+"|"
                +self.seller_city_name)

    def description_parser(self):
        """
        """
        return MerliDescription(self.raw["description"])

    def questions_parser(self):
        """
        """
        return MerliQuestion(self.raw["questions"])



class MerliDescription(Parser):
    """
    """
    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def plain_text_parser(self):
        """
        """
        self.plain_text_cloud=self.word_list(self.raw["plain_text"])
        self.mention_channels=False #machine learning - ??
        return self.raw["plain_text"]

    def date_created_parser(self):
        """
        """
        return date_parse(self.raw["date_created"])

    def last_updated_parser(self):
        """
        """
        return date_parse(self.raw["last_updated"])

    def snapshot_parser(self):
        """
        """
        return self.raw["snapshot"]["url"]


class MerliQuestion(Parser):
    """
    """

    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def date_created_parser(self):
        """
        """
        return date_parse(self._raw["date_created"])

    def status_parser(self):
        """
        """
        return self.raw["status"].lower()

    def answer_parser(self):
        """
        """
        answer_obj=self.raw["answer"]
        answer_obj["status"]=answer_obj["status"].lower()
        answer_obj["date_created"]=date_parse(answer_obj["date_created"])
        answer_obj=["text_cloud"]=self.world_list(answer_obj["text"])
        return answer_obj

    def text_parser(self):
        """
        """
        self.text_cloud=self.world_list(self.raw["text"])
        return self.raw["text"]


class MerliUser:
    """
    """
    pass
