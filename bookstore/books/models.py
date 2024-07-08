from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    book_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cover_pic = models.ImageField(upload_to='cover_pics/', blank=True, null=True)
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField()
    author_contact = models.CharField(max_length=15)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.book_id:
            last_book = Book.objects.all().order_by('id').last()
            if not last_book:
                self.book_id = 'Book00001'
            else:
                last_id = int(last_book.book_id.replace('Book', ''))
                new_id = last_id + 1
                self.book_id = 'Book' + str(new_id).zfill(5)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
