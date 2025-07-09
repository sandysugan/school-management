from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Book,BookIssue,EBook
from app.schemas import BookSchema,BookIssueSchema,EBookSchema

#-----------------------------------CRUD for books----------------------------------------------#

def create_book(db: Session, data: BookSchema):
    db_obj = Book(
        title=data.title,
        author=data.author,
        publisher=data.publisher,
        quantity=data.quantity,
        available=data.available,
        status=data.status,
        created_by=data.created_by,
        updated_by=data.updated_by,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_books(db: Session):
    return db.query(Book).filter(Book.status != "deleted").all()

def get_book_by_id(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def update_book(db: Session, id: int, data: BookSchema):
    db_obj = db.query(Book).filter(Book.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_book(db: Session, id: int, updated_by: int):
    db_obj = db.query(Book).filter(Book.id == id).first()
    if db_obj:
        db_obj.status = "deleted"
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#---------------------------------------CRUD for book_issues----------------------------------------------------------#

def create_bulk_book_issues(db: Session, issues_data: list[BookIssueSchema]):
    now = datetime.utcnow()
    issue_objs = []

    for data in issues_data:
        issue = BookIssue(
            book_id=data.book_id,
            student_id=data.student_id,
            issue_date=data.issue_date,
            due_date=data.due_date,
            return_date=data.return_date,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        issue_objs.append(issue)

    db.add_all(issue_objs)
    db.commit()
    return issue_objs

def get_all_book_issues(db: Session):
    return db.query(BookIssue).filter(BookIssue.status != "deleted").all()

def get_book_issue_by_id(db: Session, id: int):
    return db.query(BookIssue).filter(BookIssue.id == id).first()

def update_book_issue(db: Session, id: int, data: BookIssueSchema):
    db_obj = db.query(BookIssue).filter(BookIssue.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_book_issue(db: Session, id: int, updated_by: int):
    db_obj = db.query(BookIssue).filter(BookIssue.id == id).first()
    if db_obj:
        db_obj.status = "deleted"
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#---------------------------------------------CRUD for ebooks----------------------------------------------------#


def create_bulk_ebooks(db: Session, ebook_data: list[EBookSchema]):
    now = datetime.utcnow()
    ebook_objs = []

    for data in ebook_data:
        ebook = EBook(
            subject_id=data.subject_id,
            title=data.title,
            file_url=data.file_url,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        ebook_objs.append(ebook)

    db.add_all(ebook_objs)
    db.commit()
    return ebook_objs

def get_all_ebooks(db: Session):
    return db.query(EBook).filter(EBook.status == 1).all()

def get_ebook_by_id(db: Session, id: int):
    return db.query(EBook).filter(EBook.id == id).first()

def update_ebook(db: Session, id: int, data: EBookSchema):
    db_obj = db.query(EBook).filter(EBook.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_ebook(db: Session, id: int, updated_by: int):
    db_obj = db.query(EBook).filter(EBook.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False