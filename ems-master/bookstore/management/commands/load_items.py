import random
from django.core.management.base import BaseCommand
from bookstore.models import Publisher, Store, Book


class Command(BaseCommand):
    """
    This command is for inserting Publisher, Book, Store into database.
    Insert 5 Publishers, 100 Books, 10 Stores.
    """

    def handle(self, *args, **options):
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()

        #Adding Publisher
        publisher = [Publisher(name=f"Publisher {i}") for i in range(1,6)]
        Publisher.objects.bulk_create(publisher)

        #Adding 20 books for each publisher
        count = 0
        books = []
        for publisher in Publisher.objects.all():
            for i in range(20):
                count += 1
                books.append(Book(name=f"Book {count}", price = random.randint(50,500), publisher = publisher))
        Book.objects.bulk_create(books)

        #Create 10 Stores and insert 10 books in each Store
        books = list(Book.objects.all())  # All 100 books will come
        for i in range(1,11):
            ten_books = [books.pop(0) for _ in range(10)] # Will pop 0th element from books 10 times. To get 10 books
            print('ten_books:',ten_books)
            store = Store.objects.create(name=f"Store {i}")
            print('store:',store)
            store.books.set(ten_books)
            store.save()