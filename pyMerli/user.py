import requests

class User:
    """
    """
    _headers={
        "User_Agent":"pyMerli",
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
