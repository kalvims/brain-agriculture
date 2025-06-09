from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.plantation_repository import PlantationRepository
from app.db.repositories.season_repository import SeasonRepository
from app.schemas.plantation import PlantationCreate


class PlantationService:
    def __init__(self, db: Session):
        self.db = db
        self.plantation_repo = PlantationRepository(db)
        self.season_repo = SeasonRepository(db)

    def create_plantation(self, plantation: PlantationCreate):
        """
        Cria uma nova cultura.

        Args:
            plantation (PlantationCreate): Dados da cultura a ser criada.

        Returns:
            Plantation: A cultura criada.
        """
        logger.info("Tentando criar uma nova cultura")
        created_plantation = self.plantation_repo.create_plantation(plantation)
        logger.info("Cultura criada com sucesso")
        return created_plantation

    def get_plantation_by_id(self, plantation_id: int):
        """
        Busca uma cultura pelo seu ID.

        Args:
            plantation_id (int): ID da cultura a ser buscada.

        Returns:
            Plantation: A cultura encontrada.

        Raises:
            HTTPException: Se a cultura não for encontrada.
        """
        logger.info(f"Buscando cultura por ID: {plantation_id}")
        plantation = self.plantation_repo.get_plantation_by_id(plantation_id)
        if not plantation:
            logger.error(f"Cultura não encontrada: ID {plantation_id}")
            raise HTTPException(status_code=404, detail="Plantation not found")
        return plantation

    def list_plantations(self, offset: int = 0, limit: int = 100):
        """
        Lista todas as culturas com paginação.

        Args:
            offset (int): Número de registros a serem pulados (padrão: 0).
            limit (int): Número máximo de registros a serem retornados (padrão: 100).

        Returns:
            list[Plantation]: Lista de culturas.
        """
        logger.info("Listando todas as culturas")
        return self.plantation_repo.list_plantations(
            offset=offset, limit=limit)

    def update_plantation(self, plantation_id: int,
                          plantation: PlantationCreate):
        """
        Atualiza uma cultura existente.

        Args:
            plantation_id (int): ID da cultura a ser atualizada.
            plantation (PlantationCreate): Novos dados da cultura.

        Returns:
            Plantation: A cultura atualizada.

        Raises:
            HTTPException: Se a cultura não for encontrada.
        """
        logger.info(f"Atualizando cultura ID: {plantation_id}")
        updated_plantation = self.plantation_repo.update_plantation(
            plantation_id, plantation
        )
        if not updated_plantation:
            logger.error(f"Cultura não encontrada: ID {plantation_id}")
            raise HTTPException(status_code=404, detail="Plantation not found")
        logger.info("Cultura atualizada com sucesso")
        return updated_plantation

    def remove_plantation(self, plantation_id: int):
        """
        Remove uma cultura existente.

        Args:
            plantation_id (int): ID da cultura a ser removida.

        Returns:
            Plantation: A cultura removida.

        Raises:
            HTTPException: Se a cultura não for encontrada ou se houver registros relacionados.
        """
        logger.info(f"Removendo cultura ID: {plantation_id}")
        plantation = self.plantation_repo.get_plantation_by_id(plantation_id)
        if not plantation:
            logger.error(f"Cultura não encontrada: ID {plantation_id}")
            raise HTTPException(status_code=404, detail="plantation not found")
        if plantation.farm_plantations:
            logger.error(
                "Não é possível deletar a cultura porque há registros relacionados"
            )
            raise HTTPException(
                status_code=400,
                detail="Cannot delete plantation because it has related records",
            )

        deleted_plantation = self.plantation_repo.remove_plantation(
            plantation_id)
        if not deleted_plantation:
            logger.error(f"Cultura não encontrada: ID {plantation_id}")
            raise HTTPException(status_code=404, detail="Plantation not found")
        logger.info("Cultura removida com sucesso")
        return deleted_plantation

    def get_plantation_seasons(self, plantation_id: int):
        """
        Busca as safras associadas a uma cultura.

        Args:
            plantation_id (int): ID da cultura.

        Returns:
            list[FarmPlantation]: Lista de safras associadas à cultura.

        Raises:
            HTTPException: Se a cultura não for encontrada.
        """
        logger.info(f"Buscando safras da cultura ID: {plantation_id}")
        plantation = self.plantation_repo.get_plantation_by_id(plantation_id)
        if not plantation:
            logger.error(f"Cultura não encontrada: ID {plantation_id}")
            raise HTTPException(status_code=404, detail="Plantation not found")
        return plantation.farm_plantations
