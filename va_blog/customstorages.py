from django.conf import settings
from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    host = "s3.{}.amazonaws.com".format(config('AWS_REGION'))

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    host = "s3.{}.amazonaws.com".format(config('AWS_REGION'))