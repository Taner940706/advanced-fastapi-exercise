from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: str
    title: str
    author: str
    description: str
    rating: str
    published_date: str

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="id is not needed")
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=10)
    description: str = Field(min_length=1, max_length=5)
    rating: int = Field(gt=0, lt=10)
    published_date: int = Field(gt=1900, lt=2023)

    class Config:
        schema_extra = {
            'example': {
                'title': "New book title",
                'author': "New book author",
                'description': "New Book description",
                'rating': 5,
                'published_date': 2023
            }
        }


BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 6, 1990),
    Book(2, "Title Two", "Author Two", "Description Two", 5, 2020),
    Book(3, "Title Three", "Author Three", "Description Three", 4, 2000),
    Book(4, "Title Four", "Author Four", "Description Four", 3, 1975),
    Book(5, "Title Five", "Author Five", "Description Five", 2, 1919),
]


@app.get('/books', status_code=status.HTTP_200_OK)
def get_all_books():
    return BOOKS


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
def create_book(request: BookRequest):
    new_book = Book(**request.dict())
    BOOKS.append(get_id(new_book))


def get_id(book: Book):
    if len(BOOKS) == 0:
        book.id = 1
    else:
        book.id = BOOKS[-1].id + 1
    return book


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="The id not found!")


@app.get('/books/', status_code=status.HTTP_200_OK)
def get_books_by_rating(rating: int = Path(lt=0, gt=10)):
    return_books = []
    for book in BOOKS:
        if book.rating == rating:
            return_books.append(book)
    return return_books


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book doesn't updated")


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


@app.get('/books/get_book/{published_date}', status_code=status.HTTP_200_OK)
def get_book_by_published_date(published_date: int = Path(lt=1900, gt=2023)):
    for book in BOOKS:
        if book.published_date == published_date:
            return book
