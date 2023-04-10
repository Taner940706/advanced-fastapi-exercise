from fastapi import FastAPI, Body

app = FastAPI()


class Book:
    id: str
    title: str
    author: str
    description: str
    rating: str

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 6),
    Book(2, "Title Two", "Author Two", "Description Two", 5),
    Book(3, "Title Three", "Author Three", "Description Three", 4),
    Book(4, "Title Four", "Author Four", "Description Four", 3),
    Book(5, "Title Five", "Author Five", "Description Five", 2),
]


@app.get('/books')
def get_all_books():
    return BOOKS


@app.post('/create-book')
def create_book(request=Body()):
    BOOKS.append(request)
