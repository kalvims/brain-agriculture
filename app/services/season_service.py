from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.season_repository import SeasonRepository
from app.schemas.season import SeasonCreate


class SeasonService:
    def __init__(self, db: Session):
        self.db = db
        self.season_repo = SeasonRepository(db)

    def create_season(self, season: SeasonCreate):
        """
        Cria uma nova safra.

        Args:
            season (SeasonCreate): Dados da safra a ser criada.

        Returns:
            Season: A safra criada.
        """
        logger.info("Tentando criar uma nova safra")
        created_season = self.season_repo.create_season(season)
        logger.info("Safra criada com sucesso")
        return created_season

    def get_season_by_id(self, season_id: int):
        """
        Busca uma safra pelo seu ID.

        Args:
            season_id (int): ID da safra a ser buscada.

        Returns:
            Season: A safra encontrada.

        Raises:
            HTTPException: Se a safra não for encontrada.
        """
        logger.info(f"Buscando safra por ID: {season_id}")
        season = self.season_repo.get_season_by_id(season_id)
        if not season:
            logger.error(f"Safra não encontrada: ID {season_id}")
            raise HTTPException(status_code=404, detail="Safra não encontrada")
        return season

    def list_seasons(self, offset: int = 0, limit: int = 100):
        """
        Lista todas as safras com paginação.

        Args:
            offset (int): Número de registros a serem pulados (padrão: 0).
            limit (int): Número máximo de registros a serem retornados (padrão: 100).

        Returns:
            list[Season]: Lista de safras.
        """
        logger.info("Listando todas as safras")
        return self.season_repo.list_seasons(offset=offset, limit=limit)

    def update_season(self, season_id: int, season: SeasonCreate):
        """
        Atualiza uma safra existente.

        Args:
            season_id (int): ID da safra a ser atualizada.
            season (SeasonCreate): Novos dados da safra.

        Returns:
            Season: A safra atualizada.

        Raises:
            HTTPException: Se a safra não for encontrada.
        """
        logger.info(f"Atualizando safra ID: {season_id}")
        updated_season = self.season_repo.update_season(season_id, season)
        if not updated_season:
            logger.error(f"Safra não encontrada: ID {season_id}")
            raise HTTPException(status_code=404, detail="Safra não encontrada")
        logger.info("Safra atualizada com sucesso")
        return updated_season

    def remove_season(self, season_id: int):
        """
        Remove uma safra existente.

        Args:
            season_id (int): ID da safra a ser removida.

        Returns:
            Season: A safra removida.

        Raises:
            HTTPException: Se a safra não for encontrada ou se houver registros relacionados.
        """
        logger.info(f"Removendo safra ID: {season_id}")
        season = self.season_repo.get_season_by_id(season_id)
        if not season:
            logger.error(f"Safra não encontrada: ID {season_id}")
            raise HTTPException(status_code=404, detail="Safra não encontrada")
        if season.farm_plantations:
            logger.error(
                "Não é possível deletar a safra porque há registros relacionados"
            )
            raise HTTPException(
                status_code=400,
                detail="Não é possível deletar a safra porque há registros relacionados",
            )

        deleted_season = self.season_repo.remove_season(season_id)
        if not deleted_season:
            logger.error(f"Falha ao deletar a safra: ID {season_id}")
            raise HTTPException(
                status_code=400,
                detail="Falha ao deletar a safra")
        logger.info("Safra removida com sucesso")
        return deleted_season

    def get_season_plantations(self, season_id: int):
        """
        Busca as culturas associadas a uma safra.

        Args:
            season_id (int): ID da safra.

        Returns:
            list[FarmPlantation]: Lista de culturas associadas à safra.

        Raises:
            HTTPException: Se a safra não for encontrada.
        """
        logger.info(f"Buscando culturas da safra ID: {season_id}")
        season = self.season_repo.get_season_by_id(season_id)
        if not season:
            logger.error(f"Safra não encontrada: ID {season_id}")
            raise HTTPException(status_code=404, detail="Safra não encontrada")
        return season.farm_plantations
