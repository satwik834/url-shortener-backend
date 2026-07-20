from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.link import URLRequest, LinkResponse
from app.core.rate_limiter import check_rate_limit
from app.core.dependencies import get_current_user_id
from app.services.link_service import resolve_short_code
import app.crud.link as crud_link

router = APIRouter()

@router.post('/shorten')
def shorten(
    request: URLRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    check_rate_limit(current_user_id)
    try:
        long_url = str(request.long_url)
        # Optimized to create, encode, and save in a single transaction/commit
        link = crud_link.create_link(db=db, long_url=long_url, user_id=current_user_id)
        return {"short_url": link.short_url}
    except Exception as e:
        print("Shorten exception:", e)
        raise HTTPException(status_code=500, detail="failed to create short url")

@router.get("/links", response_model=list[LinkResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return crud_link.get_links_by_user(db=db, user_id=current_user_id)

@router.get('/{short_code}')
def redirect(short_code: str, db: Session = Depends(get_db)):
    link = resolve_short_code(db=db, short_code=short_code)
    if not link:
        raise HTTPException(status_code=404, detail='Link not found')
    return RedirectResponse(url=link, status_code=302)

@router.delete("/{short_code}")
def delete(
    short_code: str,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    link = crud_link.get_link_by_short_url(db=db, short_url=short_code)
    if not link:
        raise HTTPException(status_code=404, detail='link not found')
    if link.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    crud_link.delete_link(db=db, short_url=short_code)
    return {"message": "deleted"}
