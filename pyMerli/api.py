import copy
import time
import requests
from datetime import datetime
from pyMerli.item import Offer

class Search:
    """
    """
    _search_url="https://api.mercadolibre.com/sites/"\
              "{country_id}/search?q={keyword}"\
              "&category={category_id}&offset={offset}&limit={page_size}"
    _str_date="%d-%m-%YT%H:%M"

    def __init__(self, keyword, country_id, category_id, **kwargs):
        """
        ML page size default is 50
        """
        self.page_count=0
        self.item_count=0
        self.keyword=keyword
        self.country_id=country_id
        self.category_id=category_id
        self.user_profile=kwargs.get("user_profile", True)
        self.description=kwargs.get("description", True)
        self.categories=kwargs.get("categories", True)
        self.questions=kwargs.get("questions", True)
        self.no_token=kwargs.get("no_token", True)
        self.offset=kwargs.get("offset",0)
        self.limit=kwargs.get("limit", 0)
        self.page_size=kwargs.get("page_size", 50)
        self.tags=kwargs.get("tags",{})
        self.session=requests.Session()
        self.session.headers={
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "User-Agent":"pyMerli"
        }
        self.metadata={
            "request":{
                "country_id":self.country_id,
                "category_id":self.category_id,
                "keyword":self.keyword
            }
        }

    def __del__(self):
        """
        """
        self.session.close()

    def _mount_search_url(self):
        """
        """
        _url=self._search_url.format(country_id=self.country_id,
                                     keyword=self.keyword,
                                     category_id=self.category_id,
                                     offset=self.offset,
                                     page_size=self.page_size)


        self.url=_url

    def offers(self, byOffer=False):
        """
        """
        while (True):
            self._mount_search_url()
            response=self.session.get(self.url)
            response.raise_for_status()
            jsonResponse=response.json()
            paging=jsonResponse["paging"]
            total=paging["total"]
            self.metadata["tags"]=self.tags
            self.metadata["request"]["total"]=total
            results=self.enrich_results(jsonResponse["results"])
            if byOffer:
                for result in results: yield result
            else:
                yield results
            self.offset=paging["offset"]+paging["limit"]
            #results limit
            if total <= self.offset:break
            #client limit
            if self.limit and self.limit < self.offset:break
            #no token limit
            if self.no_token and self.offset>1000:break
            self.page_count+=1
            time.sleep(0.0001)

    def enrich_results(self, results):
        """
        """
        parsed_results=[]
        captured_at=datetime.utcnow().strftime(self._str_date)
        for result in results:
            self.item_count+=1
            result["metadata"]=copy.deepcopy(self.metadata)
            result["metadata"]["page_url"]=self.url
            result["metadata"]["captured_at"]=captured_at
            result["metadata"]["item_count"]=self.item_count
            result["metadata"]["page_count"]=self.page_count
            if self.description:
                item_id=result["id"]
                result["description"]=Offer.description(item_id)
            if self.questions:
                result["questions"]=[]
                for question in Offer.questions(item_id):
                    result["questions"].append(question)
            if self.categories:
                result["categories"]=Offer.categories(result["category_id"])
            if self.user_profile:
                result["user_profile"]=User.details(result["seller"]["id"])
            parsed_results.append(result)
            if self.limit and self.limit <= self.item_count:break
        return parsed_results

class User:
    """
    """
    _headers={
        "User-Agent":"pyMerli",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    _user_url="https://api.mercadolibre.com/users/{user_id}"

    @classmethod
    def details(cls, user_id):
        """
        """
        _url=cls._user_url.format(user_id=user_id)
        response=requests.get(_url, headers=cls._headers)
        response.raise_for_status()
        jsonResponse=response.json()
        return jsonResponse
