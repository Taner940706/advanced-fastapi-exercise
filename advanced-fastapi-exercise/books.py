from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

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


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is not needed")
    title: str = Field(min_length=1)
    author: str = Field(min_length=3, max_length=10)
    description: str = Field(min_length=1, max_length=5)
    rating: int = Field(gt=0, lt=10)

    class Config:
        schema_extra = {
            'example': {
                'title': "New book title",
                'author': "New book author",
                'description': "New Book description",
                'rating': 5
            }
        }


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
def create_book(request: BookRequest):
    new_book = Book(**request.dict())
    BOOKS.append(get_id(new_book))


def get_id(book: Book):
    if len(BOOKS) == 0:
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1
    return book
