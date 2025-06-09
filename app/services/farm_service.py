from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.farm_repository import FarmRepository
from app.db.repositories.plantation_repository import PlantationRepository
from app.db.repositories.productor_repository import ProductorRepository
from app.db.repositories.season_repository import SeasonRepository
from app.schemas.farm import Farm, FarmCreate, FarmPlantation
from app.schemas.farm_plantation_season import FarmPlantationSeasonCreate


class FarmService:
    def __init__(self, db: Session):
        self.db = db
        self.farm_repo = FarmRepository(db)
        self.productor_repo = ProductorRepository(db)

    def area_validate(self, farm: FarmCreate):
        """
        Valida se a soma das áreas de vegetação e cultivável é menor ou igual à área total.

        Args:
            farm (FarmCreate): Dados da fazenda a serem validados.

        Returns:
            bool: True se a validação for bem-sucedida, False caso contrário.
        """
        return (farm.vegetation_area + farm.arable_area) <= farm.total_area

    def create_farm(self, farm: FarmCreate):
        """
        Cria uma nova fazenda.

        Args:
            farm (FarmCreate): Dados da fazenda a ser criada.

        Returns:
            Farm: A fazenda criada.

        Raises:
            HTTPException: Se o produtor não for encontrado ou se a validação da área falhar.
        """
        logger.info(
            f"Tentando criar uma nova fazenda para o produtor ID: {farm.productor_id}"
        )
        if not self.productor_repo.productor_exists(farm.productor_id):
            logger.error(f"Produtor não encontrado: ID {farm.productor_id}")
            raise HTTPException(status_code=404, detail="Productor not found")

        if not self.area_validate(farm):
            logger.error(
                "Área total é menor que a soma das áreas de vegetação e cultivável"
            )
            raise HTTPException(
                status_code=400,
                detail="The total area is less than the combined area of vegetation and arable land",
            )

        logger.info("Fazenda criada com sucesso")
        return self.farm_repo.create_farm(farm)

    def add_plantation(
        self, farm_id: int, plantation_season: FarmPlantationSeasonCreate
    ):
        """
        Adiciona uma cultura a uma safra específica em uma fazenda.

        Args:
            farm_id (int): ID da fazenda.
            plantation_season (FarmPlantationSeasonCreate): Dados da cultura e safra a serem adicionados.

        Returns:
            FarmPlantationSeason: A relação entre fazenda, cultura e safra criada.

        Raises:
            HTTPException: Se a fazenda, cultura ou safra não forem encontradas, ou se a cultura já existir na safra.
        """
        logger.info(f"Tentando adicionar cultura à fazenda ID: {farm_id}")
        plantation_repo = PlantationRepository(self.db)
        season_repo = SeasonRepository(self.db)

        if not self.get_farm_by_id(farm_id):
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")

        if not plantation_repo.get_plantation_by_id(
                plantation_season.plantation_id):
            logger.error(
                f"Cultura não encontrada: ID {plantation_season.plantation_id}"
            )
            raise HTTPException(status_code=404, detail="Plantation not found")

        if not season_repo.get_season_by_id(plantation_season.season_id):
            logger.error(
                f"Safra não encontrada: ID {plantation_season.season_id}")
            raise HTTPException(status_code=404, detail="Season not found")

        if self.farm_repo.farm_plantation_exists(farm_id, plantation_season):
            logger.error("Cultura já existe nesta safra")
            raise HTTPException(
                status_code=400, detail="Plantation already exists in this season"
            )

        logger.info("Cultura adicionada com sucesso")
        return self.farm_repo.add_plantation(farm_id, plantation_season)

    def get_farm_by_id(self, farm_id: int):
        """
        Busca uma fazenda pelo seu ID.

        Args:
            farm_id (int): ID da fazenda a ser buscada.

        Returns:
            Farm: A fazenda encontrada.

        Raises:
            HTTPException: Se a fazenda não for encontrada.
        """
        logger.info(f"Buscando fazenda por ID: {farm_id}")
        farm = self.farm_repo.get_farm_by_id(farm_id)
        if not farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")
        return farm

    def list_farms(self, offset: int = 0, limit: int = 100):
        """
        Lista todas as fazendas com paginação.

        Args:
            offset (int): Número de registros a serem pulados (padrão: 0).
            limit (int): Número máximo de registros a serem retornados (padrão: 100).

        Returns:
            list[Farm]: Lista de fazendas.
        """
        logger.info("Listando todas as fazendas")
        return self.farm_repo.list_farms(offset=offset, limit=limit)

    def update_farm(self, farm_id: int, farm: FarmCreate):
        """
        Atualiza uma fazenda existente.

        Args:
            farm_id (int): ID da fazenda a ser atualizada.
            farm (FarmCreate): Novos dados da fazenda.

        Returns:
            Farm: A fazenda atualizada.

        Raises:
            HTTPException: Se o produtor não for encontrado, a validação da área falhar ou a fazenda não for encontrada.
        """
        logger.info(f"Atualizando fazenda ID: {farm_id}")
        if not self.productor_repo.productor_exists(farm.productor_id):
            logger.error(f"Produtor não encontrado: ID {farm.productor_id}")
            raise HTTPException(status_code=404, detail="Productor not found")

        if not self.area_validate(farm):
            logger.error(
                "Área total é menor que a soma das áreas de vegetação e cultivável"
            )
            raise HTTPException(
                status_code=400,
                detail="The total area is less than the combined area of vegetation and arable land",
            )

        updated_farm = self.farm_repo.update_farm(farm_id, farm)
        if not updated_farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")

        logger.info("Fazenda atualizada com sucesso")
        return updated_farm

    def remove_farm(self, farm_id: int):
        """
        Remove uma fazenda existente.

        Args:
            farm_id (int): ID da fazenda a ser removida.

        Returns:
            Farm: A fazenda removida.

        Raises:
            HTTPException: Se a fazenda não for encontrada ou se houver registros relacionados.
        """
        logger.info(f"Removendo fazenda ID: {farm_id}")
        farm = self.farm_repo.get_farm_by_id(farm_id)
        if not farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")
        if farm.farm_plantations:
            logger.error(
                "Não é possível deletar a fazenda porque há registros relacionados"
            )
            raise HTTPException(
                status_code=400,
                detail="Cannot delete farm because it has related records",
            )

        deleted_farm = self.farm_repo.remove_farm(farm_id)
        if not deleted_farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")

        logger.info("Fazenda removida com sucesso")
        return deleted_farm

    def get_farm_plantations(self, farm_id: int):
        """
        Busca as culturas associadas a uma fazenda.

        Args:
            farm_id (int): ID da fazenda.

        Returns:
            list[FarmPlantation]: Lista de culturas associadas à fazenda.

        Raises:
            HTTPException: Se a fazenda não for encontrada.
        """
        logger.info(f"Buscando plantações da fazenda ID: {farm_id}")
        farm = self.farm_repo.get_farm_by_id(farm_id)
        if not farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")
        return self.get_plantations(farm)

    def get_plantations(self, farm: Farm) -> list[FarmPlantation]:
        """
        Processa as plantações de uma fazenda, organizando-as por cultura e safra.

        Args:
            farm (Farm): A fazenda cujas plantações serão processadas.

        Returns:
            list[FarmPlantation]: Uma lista de dicionários contendo as culturas e suas safras associadas.
        """
        logger.info(f"Processando plantações da fazenda ID: {farm.id}")
        farm_plantations_dict = {}
        for fps in farm.farm_plantations:
            if fps.plantation and fps.season:
                plantation_id = fps.plantation.id

                if plantation_id not in farm_plantations_dict:
                    farm_plantations_dict[plantation_id] = {
                        "id": fps.plantation.id,
                        "name": fps.plantation.name,
                        "description": fps.plantation.description,
                        "seasons": [],
                    }

                farm_plantations_dict[plantation_id]["seasons"].append(
                    {
                        "id": fps.season.id,
                        "description": fps.season.description,
                        "year": fps.season.year,
                    }
                )

        farm_plantations_output = list(farm_plantations_dict.values())
        return farm_plantations_output

    def get_farm_seasons(self, farm_id: int):
        """
        Busca as safras associadas a uma fazenda.

        Args:
            farm_id (int): ID da fazenda.

        Returns:
            list[FarmSeason]: Lista de safras associadas à fazenda.

        Raises:
            HTTPException: Se a fazenda não for encontrada.
        """
        logger.info(f"Buscando safras da fazenda ID: {farm_id}")
        farm = self.farm_repo.get_farm_by_id(farm_id)
        if not farm:
            logger.error(f"Fazenda não encontrada: ID {farm_id}")
            raise HTTPException(status_code=404, detail="Farm not found")
        return self.get_seasons(farm)

    def get_seasons(self, farm: Farm) -> list[FarmPlantation]:
        """
        Processa as safras de uma fazenda, organizando-as por safra e cultura.

        Args:
            farm (Farm): A fazenda cujas safras serão processadas.

        Returns:
            list[FarmPlantation]: Uma lista de dicionários contendo as safras e suas culturas associadas.
        """
        logger.info(f"Processando safras da fazenda ID: {farm.id}")
        farm_seasons_dict = {}
        for fps in farm.farm_plantations:
            if fps.plantation and fps.season:
                season_id = fps.season.id

                if season_id not in farm_seasons_dict:
                    farm_seasons_dict[season_id] = {
                        "id": fps.season.id,
                        "year": fps.season.year,
                        "description": fps.season.description,
                        "plantations": [],
                    }

                farm_seasons_dict[season_id]["plantations"].append(
                    {
                        "id": fps.plantation.id,
                        "description": fps.plantation.description,
                        "name": fps.plantation.name,
                    }
                )

        farm_seasons_output = list(farm_seasons_dict.values())
        return farm_seasons_output
