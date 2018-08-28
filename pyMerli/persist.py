from custodi.smallBoto import S3Bucket

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
        self.merli=merliObj
        self.s3=self._s3(self._bucket)

    def save(self, key_field):
        """
        """
        self.s3.uploadJson(self.merli.raw, getattr(self.merli, key_field))
        self.postSave.message="[+] S3 Persist Bucket: {} | Key: {}".format(
                                                    self._bucket, key_field)
