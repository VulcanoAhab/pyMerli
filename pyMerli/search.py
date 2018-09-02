import time
import requests
from datetime import datetime
from item import Offer

class Request:
    """
    """
    _search_url="https://api.mercadolibre.com/sites/"\
              "{country_id}/search?q={keyword}"\
              "&category={category_id}&offset={offset}"
    _str_date="%d-%m-%YT%H:%M"

    def __init__(self, keyword, country_id, category_id, offset):
        """
        """
        self.metadata={}
        self.offset=offset
        self.keyword=keyword
        self.country_id=country_id
        self.category_id=category_id

    def _mount_search_url(self):
        """
        """
        _url=self._search_url.format(country_id=self.country_id,
                                  keyword=self.keyword,
                                  category_id=self.category_id,
                                  offset=self.offset)
        _metaDict={
            "country_id":self.country_id, "category_id":self.category_id,
            "offset":self.offset, "keyword":self.keyword
        }
        self.url=_url
        self.metadata["request"]=_metaDict

    def offers(self, limit=0, description=True, question=True, no_token=True):
        """
        """
        session=requests.Session()
        session.headers["User-Agent"]="pyMerli"
        page_count=0
        item_count=0
        while (True):
            self._mount_search_url()
            response=session.get(self.url)
            response.raise_for_status()
            jsonResponse=response.json()
            paging=jsonResponse["paging"]
            results=jsonResponse["results"]
            total=paging["total"]
            for result in results:
                item_count+=1
                self.metadata["request"]["item_count"]=item_count
                self.metadata["request"]["page_count"]=page_count
                found_at=datetime.utcnow().strftime(self._str_date)
                self.metadata["request"]["found_at"]=found_at
                result["request"]=self.metadata["request"]
                if description:
                    item_id=result["id"]
                    result["description"]=Offer.description(item_id)
                if question:
                    result["questions"]=[]
                    for question in Offer.questions(item_id):
                        result["questions"].append(question)
                yield result
                if limit and limit <= item_count:break
            self.offset=paging["offset"]+paging["limit"]
            if total <= self.offset:break
            if no_token and self.offset>1000:break
            time.sleep(0.01)
            page_count+=1
