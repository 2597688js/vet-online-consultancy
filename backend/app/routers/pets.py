import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Pet, PetPhoto, User
from app.schemas import PetCreateRequest, PetOut
from app.storage import save_pet_photo

router = APIRouter(prefix="/api/pets", tags=["pets"])

MAX_PHOTOS_PER_UPLOAD = 6


def _get_owned_pet(pet_id: uuid.UUID, current_user: User, db: Session) -> Pet:
    pet = db.get(Pet, pet_id)
    if pet is None or pet.deleted_at is not None or pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@router.post("", response_model=PetOut, status_code=status.HTTP_201_CREATED)
def create_pet(
    payload: PetCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Pet:
    pet = Pet(owner_id=current_user.id, **payload.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("", response_model=list[PetOut])
def list_pets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Pet]:
    return (
        db.query(Pet)
        .filter(Pet.owner_id == current_user.id, Pet.deleted_at.is_(None))
        .order_by(Pet.created_at.desc())
        .all()
    )


@router.post("/{pet_id}/photos", response_model=PetOut)
async def upload_pet_photos(
    pet_id: uuid.UUID,
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Pet:
    pet = _get_owned_pet(pet_id, current_user, db)

    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided")
    if len(files) > MAX_PHOTOS_PER_UPLOAD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Upload at most {MAX_PHOTOS_PER_UPLOAD} photos at a time"
        )

    for file in files:
        url = await save_pet_photo(pet.id, file)
        db.add(PetPhoto(pet_id=pet.id, url=url))

    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}/photos/{photo_id}", response_model=PetOut)
def delete_pet_photo(
    pet_id: uuid.UUID,
    photo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Pet:
    pet = _get_owned_pet(pet_id, current_user, db)

    photo = db.get(PetPhoto, photo_id)
    if photo is None or photo.pet_id != pet.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    db.delete(photo)
    db.commit()
    db.refresh(pet)
    return pet
