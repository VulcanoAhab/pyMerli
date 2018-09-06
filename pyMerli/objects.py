
import re
import json
import copy
import string
from datetime import datetime
from dateutil.parser import parse as date_parse

class Parser:
    """
    """
    _puncs=list(string.punctuation)
    _cloud=re.compile("([^{}\s]+[\S]+[^{}\s]+)|([\w\d]+)".format(
                                            _puncs, _puncs), re.M)
    @classmethod
    def word_list(cls, text_in):
        """
        """
        word_list=[]
        tuple_list=cls._cloud.findall(text_in.lower())
        for tup in tuple_list:
            if not any(tup):continue
            if tup[0] and len(tup[0])>3:word_list.append(tup[0])
            else:
                if tup[1] and len(tup[1])>3:word_list.append(tup[1])
        return word_list

    def __init__(self, raw_obj):
        """
        """
        self.raw=raw_obj
        self._process()

    def _process(self):
        """
        """
        self._raw_fields=[]
        self._raw_fields_count=0
        for key,value in self.raw.items():
            try:
                parsed=getattr(self, key+"_parser")(value)
                setattr(self, key, parsed)
            except AttributeError:
                setattr(self, key, value)
            self._raw_fields.append(key)
            self._raw_fields_count+=1

    @property
    def toDict(self):
        """
        """
        full_obj=copy.deepcopy(self.__dict__)
        full_obj.pop("raw")
        return full_obj

    @property
    def _fields(self):
        """
        """
        return [f for f in self.__dict__
                if f not in ["raw", "_raw_fields", "_raw_fields_count"]]


class MerliOffer(Parser):
    """
    """
    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def __repr__(self):
        """
        """
        return "<{}:{}>".format(self.__class__.__name__, self.id)

    @property
    def toDict(self):
        """
        """
        offer=copy.deepcopy(self.__dict__)
        offer["description"]=copy.deepcopy(self.description.toDict)
        offer["categories"]=copy.deepcopy(self.categories.toDict)
        offer["questions"]=copy.deepcopy(self.questions.toDict)
        full_obj.pop("raw")
        return full_obj

    def title_parser(self, value):
        """
        """
        self.title_cloud=self.word_list(self.raw["title"])
        return value

    def attributes_parser(self, value):
        """
        """
        attrs=[]
        for attr in value:
            key=attr["id"].lower()
            value=attr["value_name"]
            setattr(self, key, value)
            attrs.append(key)
        if attrs:
            return "|".join([getattr(self, k)
                             for k in sorted(attrs)
                             if getattr(self, k)])
        return "no_attributes"

    def site_id_parser(self, value):
        """
        """
        return value.lower()

    def currency_id_parser(self, value):
        """
        """
        return value.lower()

    def stop_time_parser(self, value):
        """
        """
        return date_parse(value)

    def reviews_parser(self, value):
        """
        """
        revis=value
        self.reviews_total=revis["total"]
        self.reviews_ratio=revis["rating_average"]
        return str(self.reviews_ratio)+"|"+str(self.reviews_total)

    def installments_parser(self, value):
        """
        """
        insta=value
        self.installments_amount=insta["amount"]
        self.installments_quantity=insta["quantity"]
        self.installments_currency=insta["currency_id"].lower()
        insta["currency_id"]=self.installments_currency
        return (self.installments_currency+"|"
               +str(self.installments_amount)+"|"
               +str(self.installments_quantity))

    def seller_parser(self, value):
        """
        """
        self.seller_id=value["id"]
        return value["id"]

    def address_parser(self, value):
        """
        """
        addr=value
        self.location_state_id=addr["state_id"].lower()
        self.location_state_name=addr["state_name"].lower()
        self.location_city_id=addr["city_id"]
        self.location_city_name=addr["city_name"].lower()
        return self.location_city_name+"|"+self.location_state_name

    def shipping_parser(self, value):
        """
        """
        ships=value
        self.free_shipping=ships["free_shipping"]
        self.shipping_mode=ships["mode"]
        return str(self.free_shipping)+"|"+self.shipping_mode

    def seller_address_parser(self, value):
        """
        """
        saddr=value
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

    def description_parser(self, value):
        """
        """
        return MerliDescription(value)

    def categories_parser(self, value):
        """
        """
        return MerliCategories(value)

    def questions_parser(self, value):
        """
        """
        return MerliQuestion(value)


class MerliDescription(Parser):
    """
    """
    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def __repr__(self):
        """
        """
        return "<{}:{}...>".format(self.__class__.__name__,
                                        self.plain_text[:20])

    def plain_text_parser(self, value):
        """
        """
        self.plain_text_cloud=self.word_list(value)
        self.mention_channels=False #machine learning - ??
        return value

    def date_created_parser(self, value):
        """
        """
        return date_parse(self.raw["date_created"])

    def last_updated_parser(self, value):
        """
        """
        return date_parse(self.raw["last_updated"])

    def snapshot_parser(self, value):
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

    def __repr__(self):
        """
        """
        return "<{}:{}...>".format(self.__class__.__name__, self.text[:20])

    def text_parser(self, value):
        """
        """
        self.text_cloud=self.word_list(value)
        return value

    def date_created_parser(self, value):
        """
        """
        return date_parse(value)

    def status_parser(self, value):
        """
        """
        return value.lower()

    def answer_parser(self, value):
        """
        """
        answer_obj=value
        answer_obj["status"]=answer_obj["status"].lower()
        answer_obj["date_created"]=date_parse(answer_obj["date_created"])
        answer_obj["text_cloud"]=self.world_list(answer_obj["text"])
        return answer_obj


class MerliCategories(Parser):
    """
    """
    def __init__(self, raw_obj):
        """
        """
        super().__init__(raw_obj)

    def __repr__(self):
        """
        """
        return "<{}:{}...>".format(self.__class__.__name__,
                                self.categories_names[:20])

    def path_from_root_parser(self, value):
        """
        """
        names=[]
        for itemDict in value:names.append(itemDict["name"].lower())
        self.categories_names="|".join(names)
        return value

    def name_parser(self, value):
        """
        """
        return value.lower()


class MerliUser:
    """
    """
    pass
