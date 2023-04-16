from django.db import models
from django.core.exceptions import ValidationError
from urllib import parse

# video database model
class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True) # blank is optional, null is fine
    video_id = models.CharField(max_length=43, unique=True)

    def save(self, *args, **kwargs):
        # extract the video id from a youtube url
        # if not self.url.startswith('https://www.youtube.com/watch'):
        #     raise ValidationError(f'Not a Youtube URL {self.url}')
        url_component = parse.urlparse(self.url)
        
        if url_component.scheme != 'https':
            raise ValidationError(f'Not a Youtube URL {self.url}')
        
        if url_component.netloc != 'www.youtube.com':
            raise ValidationError(f'Not a Youtube URL {self.url}')
        
        if url_component.path != '/watch':
            raise ValidationError(f'Not a Youtube URL {self.url}')
        
        query_string = url_component.query # v=123456

        if not query_string:
            raise ValidationError(f'Invalid Youtube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True) # dictionary
        v_parameters_list = parameters.get('v') # return None if no key found, e.g abc=1234&abc=12345678

        if not v_parameters_list: # checking if None or empty list
            raise ValidationError(f'Invalid Youtube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] # string
        
        # calling this save function instead of django default save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id} Notes: {self.notes[:200]}' # notes - first 200 characters
