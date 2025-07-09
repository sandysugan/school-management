from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import BookSchema,BookIssueSchema,BulkBookIssueSchema,EBookSchema,BulkEBookSchema
from app.crud import library_crud
from app.api import deps
from app.models import User

router = APIRouter()

#--------------------------------------api for books---------------------------------------#

@router.post("/create_books")
def create_book(
    data: BookSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type !=6:
         return {"status":0, "detail":"Unauthorized User"}
    data.created_by = current_user.id
    book = library_crud.create_book(db, data)
    return {
        "status": 1,
        "msg": "Book created successfully",
        "book_id": book.id,
        "title": book.title,
        "created_by": book.created_by
    }

@router.post("/list_books")
def list_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4,6]:
         return {"status":0, "detail":"Unauthorized User"}
     
    books = library_crud.get_all_books(db)[skip:skip + limit]
    return [
        {
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "quantity": book.quantity,
            "available": book.available,
            "status": book.status,
            "created_by": book.created_by
        } for book in books
    ]

@router.post("/get_book/{id}")
def get_book(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4,6]:
         return {"status":0, "detail":"Unauthorized User"}
    
    book = library_crud.get_book_by_id(db, id)
    if not book or book.status == "deleted":
        return {"status":0,"detail":"Book not found"}

    return {
        "book_id": book.id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "quantity": book.quantity,
        "available": book.available,
        "status": book.status,
        "created_by": book.created_by,
        "created_at": book.created_at,
        "updated_by": book.updated_by,
        "updated_at": book.updated_at
    }

@router.post("update_book/{id}")
def update_book(
    id: int,
    data: BookSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type!=6:
         return {"status":0, "detail":"Unauthorized User"}
     
    data.updated_by = current_user.id
    updated_book = library_crud.update_book(db, id, data)
    if not updated_book:
        return {"status":0,"detail":"Book not found"}

    return {
        "status": 1,
        "msg": "Book updated successfully",
        "book_id": updated_book.id,
        "title": updated_book.title,
        "updated_by": updated_book.updated_by
    }

@router.post("delete_book/{id}")
def delete_book(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type !=6:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = library_crud.soft_delete_book(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Book not found"}

    return {
        "status": 1,
        "msg": "Book deleted successfully"
    }

#----------------------------------------------api for book_issues-------------------------------------------------#

@router.post("/bulk-create_book_issue")
def bulk_create_book_issues(
    data: BulkBookIssueSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=6:
         return {"status":0, "detail":"Unauthorized User"}

    for issue in data.issues:
        issue.created_by = current_user.id
        issue.updated_by = current_user.id

    created_issues = library_crud.create_bulk_book_issues(db, data.issues)
    result = [
        {
            "issue_id": i.id,
            "book_id": i.book_id,
            "student_id": i.student_id,
            "due_date": i.due_date,
            "return_date": i.return_date,
            "status": i.status
        }
        for i in created_issues
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} book issues created successfully",
        "data": result
    }

@router.post("/list_book_issue")
def list_book_issues(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,6]:
         return {"status":0, "detail":"Unauthorized User"}

    issues = library_crud.get_all_book_issues(db)[skip: skip + limit]
    return [
        {
            "issue_id": i.id,
            "book_id": i.book_id,
            "student_id": i.student_id,
            "due_date": i.due_date,
            "return_date": i.return_date,
            "status": i.status
        }
        for i in issues
    ]

@router.post("/get_book_issue/{id}")
def get_book_issue(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,4,6]:
         return {"status":0, "detail":"Unauthorized User"}

    issue = library_crud.get_book_issue_by_id(db, id)
    if not issue or issue.status == "deleted":
        return {"status":0,"detail":"Book issue record not found"}

    return {
        "issue_id": issue.id,
        "book_id": issue.book_id,
        "student_id": issue.student_id,
        "due_date": issue.due_date,
        "return_date": issue.return_date,
        "status": issue.status,
        "created_by": issue.created_by,
        "updated_by": issue.updated_by
    }

@router.post("/update_book_issue/{id}")
def update_book_issue(
    id: int,
    data: BookIssueSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1, 2]:
        return {"status":0,"detail":"Unauthorized"}

    data.updated_by = current_user.id
    updated = library_crud.update_book_issue(db, id, data)
    if not updated:
        return {"status":0,"detail":"Book issue record not found"}

    return {
        "msg": "Book issue record updated successfully",
        "issue_id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_book_issue/{id}")
def delete_book_issue(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,6]:
         return {"status":0, "detail":"Unauthorized User"}

    success = library_crud.soft_delete_book_issue(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Book issue record not found"}

    return {
        "status": 1,
        "msg": "Book issue record deleted successfully"
    }

#------------------------------------api for ebook------------------------------------------#


@router.post("/bulk_ebook_create")
def bulk_create_ebooks(
    data: BulkEBookSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,3,6]:
         return {"status":0, "detail":"Unauthorized User"}

    for ebook in data.ebooks:
        ebook.created_by = current_user.id
        ebook.updated_by = current_user.id

    created_ebooks = library_crud.create_bulk_ebooks(db, data.ebooks)
    result = [
        {
            "ebook_id": e.id,
            "title": e.title,
            "subject_id": e.subject_id,
            "file_url": e.file_url,
            "status": e.status
        }
        for e in created_ebooks
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} ebooks created successfully",
        "data": result
    }

@router.post("/list_ebooks")
def list_ebooks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4,6]:
         return {"status":0, "detail":"Unauthorized User"}

    ebooks = library_crud.get_all_ebooks(db)[skip: skip + limit]
    return [
        {
            "ebook_id": e.id,
            "title": e.title,
            "subject_id": e.subject_id,
            "file_url": e.file_url,
            "status": e.status
        }
        for e in ebooks
    ]

@router.post("/get_ebooks/{id}")
def get_ebook(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4,6]:
         return {"status":0, "detail":"Unauthorized User"}

    ebook = library_crud.get_ebook_by_id(db, id)
    if not ebook or ebook.status != 1:
        return {"status":0,"detail":"EBook not found"}

    return {
        "ebook_id": ebook.id,
        "title": ebook.title,
        "subject_id": ebook.subject_id,
        "file_url": ebook.file_url,
        "status": ebook.status,
        "created_by": ebook.created_by,
        "updated_by": ebook.updated_by
    }

@router.post("/update_ebooks/{id}")
def update_ebook(
    id: int,
    data: EBookSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,3,6]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = library_crud.update_ebook(db, id, data)
    if not updated:
        return {"status":0,"detail":"EBook not found"}

    return {
        "msg": "EBook updated successfully",
        "ebook_id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_ebooks/{id}")
def delete_ebook(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,3,6]:
         return {"status":0, "detail":"Unauthorized User"}

    success = library_crud.soft_delete_ebook(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"EBook not found"}

    return {
        "status": 1,
        "msg": "EBook deleted successfully"
    }
