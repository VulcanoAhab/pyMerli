from datetime import datetime,date
from pyMerli.objects import MerliOffer
from custodi.smallBoto import S3Bucket
from custodi.smallElastic import Basics



class S3:
    """
    """
    _bucket=""
    _s3=S3Bucket

    @classmethod
    def connection(cls, **kwargs):
        """
        """
        cls._s3.basic_conn(**kwargs)

    @classmethod
    def setBucket(cls, bucket_name):
        """
        """
        cls._bucket=bucket_name

    def __init__(self, merliObj):
        """
        """
        self.merli=MerliOffer(merliObj)
        self.s3=self._s3(self._bucket)

    def save(self, key_field):
        """
        """
        def _date_json(obj):
            """
            """
            if isinstance(obj, (datetime, date)):return obj.isoformat()
            raise TypeError ("Type %s not serializable" % type(obj))
        data=json.dumps(self.merli.toDict, default=_date_json)
        self.s3.uploadFileData(data, key_field)
        self.postSave.message="[+] S3 Persist Bucket: {} | Key: {}".format(
                                                    self._bucket, key_field)

class Es:
    """
    """

    _es=Basics

    @classmethod
    def conn(cls, *args,**kwargs):
        """
        """
        cls._es.setConn(*args,**kwargs)

    @classmethod
    def create_schema(cls):
        """
        """
        raise NotImplemented("Soon")

    @classmethod
    def setIndex(cls, index):
        """
        """
        cls._es.setIndex(index)

    @classmethod
    def setDocType(cls, doc_type):
        """
        """
        cls._es.setDoctType(doc_type)

    def __init__(self, merliObj):
        """
        """
        self.merli=MerliOffer(merliObj)

    def save(self):
        """
        """
        obj=copy.deepcopy(self.merli.toDict)
        obj.pop("raw")
        obj.pop("_fields")
        obj.pop("_raw_fields")
        obj.pop("_raw_fields_count")
        cls._es.save(obj)
