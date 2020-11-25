from django.db import models
# Create your models here.
# Source : https://medium.com/@emeruchecole9/uploading-images-to-rest-api-backend-in-react-js-b931376b5833
# Source : https://github.com/nesdis/djongo/blob/master/docs/docs/using-django-with-mongodb-gridfs.md


class File(models.Model):
    uid = models.UUIDField()
    file = models.FileField(upload_to='input_files')

    def __str__(self):
        return self.uid