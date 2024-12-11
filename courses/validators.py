import re
from rest_framework import serializers

class NoExternalLinkValidator:
    YOUTUBE_DOMAIN = "youtube.com"
    URL_REGEX = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        re.IGNORECASE
    )

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, data):
        for field in self.fields:
            if field in data:
                value = data.get(field)
                self.validate_field(field, value)

    def validate_field(self, field, value):
        urls = self.URL_REGEX.findall(value)
        for url in urls:
            if not self.is_youtube_link(url):
                raise serializers.ValidationError(
                    {field: f'Links to third-party resources other than {self.YOUTUBE_DOMAIN} are prohibited'}
                )


    def is_youtube_link(self, url):
        return self.YOUTUBE_DOMAIN in url.lower()
