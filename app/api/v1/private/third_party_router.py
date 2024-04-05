from typing import List
from fastapi import APIRouter, Depends, Path, Security, status
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.service import AuthService
from app.modules.third_party.aplication.dto import ThirdPartyRequestDTO, ThirdPartyResponseDTO
from app.modules.third_party.aplication.service import ThirdPartyService
from app.seedwork.presentation.jwt import oauth2_scheme

auth_service = AuthService()
authorized = auth_service.authorized
third_party_router = APIRouter(
    prefix='/third_parties',
    tags=["ThirdParty"],
    #dependencies=[Depends(oauth2_scheme)]
)


@third_party_router.post("", response_model=ThirdPartyResponseDTO, status_code=status.HTTP_201_CREATED
                  #,dependencies=[Security(authorized, scopes=[PermissionEnum.CREATE_SERVICE.code])]
                  )
async def create_third_party(third_party: ThirdPartyRequestDTO, db: Session = Depends(get_db)):
    third_party_service = ThirdPartyService()
    third_party_created = third_party_service.create_third_party(third_party, db)
    return third_party_created


@third_party_router.get("", response_model=List[ThirdPartyResponseDTO]
                 #,dependencies=[Security(authorized, scopes=[PermissionEnum.READ_SERVICE.code])]
                        )
async def get_third_parties(db: Session = Depends(get_db)):
    third_party_service = ThirdPartyService()
    third_parties = third_party_service.get_third_parties(db)
    return third_parties


@third_party_router.get("/{third_party_id}", response_model=ThirdPartyResponseDTO
                 #,dependencies=[Security(authorized, scopes=[PermissionEnum.READ_SERVICE.code])]
                        )
async def get_third_party_by_id(third_party_id: int = Path(ge=1), db: Session = Depends(get_db)):
    third_party_service = ThirdPartyService()
    third_party = third_party_service.get_third_party_by_id(third_party_id, db)
    return third_party