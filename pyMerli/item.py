import requests
from datetime import datetime

class Offer:
    """
    """
    _headers={
        "User_Agent":"pyMerli",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    _description_url="https://api.mercadolibre.com/"\
                     "items/{item_id}/description"
    _qa_url="https://api.mercadolibre.com/questions/"\
            "search?item_id={item_id}&offset={offset}"
    _categories_url="http://api.mercadolibre.com/categories/{category_id}"

    _item_url="https://api.mercadolibre.com/items/{item_id}"

    @classmethod
    def description(cls, item_id):
        """
        """
        _url=cls._description_url.format(item_id=item_id)
        response=requests.get(_url, headers=cls._headers)
        if response.status_code in [404,]:return {"error":"not_found"}
        response.raise_for_status()
        return response.json()

    @classmethod
    def questions(cls, item_id, offset=0):
        """
        """
        while True:
            _url=cls._qa_url.format(item_id=item_id,offset=offset)
            response=requests.get(_url, headers=cls._headers)
            response.raise_for_status()
            jsonResponse=response.json()
            limit=jsonResponse["limit"]
            total=jsonResponse["total"]
            for question in jsonResponse["questions"]:yield question
            offset+=limit
            if offset > limit:break

    @classmethod
    def categories(cls, category_id):
        """
        """
        _url=cls._categories_url.format(category_id=category_id)
        response=requests.get(_url, headers=cls._headers)
        if response.status_code in [404,]:return {"error":"not_found"}
        response.raise_for_status()
        return response.json()

    @classmethod
    def is_alive(cls, item_id):
        """
        """
        _url=cls._item_url.format(item_id=item_id)
        response=requests.get(_url, headers=cls._headers)
        if response.status_code in [404,]:return {"error":"not_found"}
        response.raise_for_status()
        item=response.json()
        expire=item["stop_time"]
        mode=item["buying_mode"]
        return {"status":"", "expire":expire, "mode":mode}
