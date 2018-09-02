from .objects import MerliOffer
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
        self.s3.uploadJson(self.merli.toDict, getattr(self.merli, key_field))
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
    def setIndex(cls, index):
        """
        """
        cls._es.setIndex(index)

    @classmethod
    def setDocType(cls, doc_type):
        """
        """
        cls._es.setDoctType(doc_type)

    @classmethod
    def setOffer(cls, offer, pre_save_fn=None):
        """
        """
        cls._offer=offer
        if pre_save_fn:
            cls._offer=pre_save_fn(offer)

    @classmethod
    def save(cls):
        """
        """
        cls._es.save(cls._offer)
