from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.repositories.farm_repository import FarmRepository
from app.db.repositories.plantation_repository import PlantationRepository
from app.schemas.reports import (
    GroundUseStatistics,
    PlantationStatistics,
    StateStatistics,
    TotalArea,
    TotalFarms,
)


class ReportsService:
    def __init__(self, db: Session):
        self.db = db
        self.farm_repo = FarmRepository(db)
        self.plantation_repo = PlantationRepository(db)

    def get_total_farms(self) -> TotalFarms:
        """
        Calcula o total de fazendas registradas.

        Returns:
            TotalFarms: Um dicionário contendo o total de fazendas.
        """
        logger.info("Calculando o total de fazendas")
        total_farms = self.farm_repo.get_total_farms()
        logger.info(f"Total de fazendas calculado: {total_farms}")
        return {"total_farms": total_farms}

    def get_total_area(self) -> TotalArea:
        """
        Calcula a área total de todas as fazendas registradas.

        Returns:
            TotalArea: Um dicionário contendo a área total das fazendas.
        """
        logger.info("Calculando a área total das fazendas")
        total_area = self.farm_repo.get_total_area()
        logger.info(f"Área total calculada: {total_area}")
        return {"total_area": total_area}

    def get_percent(self, total: float, slice: float) -> float:
        """
        Calcula a porcentagem de 'slice' em relação a 'total'.

        Args:
            total (float): O valor total.
            slice (float): O valor que representa a parte do total.

        Returns:
            float: A porcentagem de 'slice' em relação a 'total', arredondada para 2 casas decimais.
                   Retorna 0 se 'total' for zero ou negativo.
        """
        if total <= 0:
            return 0.0
        if slice < 0:
            slice = 0.0
        return round((slice / total) * 100, 2)

    def get_state_statistics(self) -> list[StateStatistics]:
        """
        Calcula estatísticas de fazendas e plantações por estado.

        Returns:
            list[StateStatistics]: Uma lista de dicionários contendo estatísticas por estado,
                                  incluindo o total de fazendas, porcentagem de fazendas,
                                  estatísticas de plantações e uso do solo.
        """
        logger.info("Calculando estatísticas por estado")
        state_statistics = {}
        total_farms = self.farm_repo.get_total_farms()
        farms_by_state = self.farm_repo.get_total_farms_by_state()
        total_plantations = self.farm_repo.get_total_plantations()

        total_area_by_state = self.farm_repo.get_total_area_by_state()
        vegetation_area_by_state = self.farm_repo.get_vegetation_area_by_state()
        arable_area_by_state = self.farm_repo.get_arable_area_by_state()
        plantations_by_state = self.farm_repo.get_plantations_by_state()

        for state, state_amount in farms_by_state:
            state_total_area = [x[1]
                                for x in total_area_by_state if x[0] == state][0]
            state_vegetation_area = [
                x[1] for x in vegetation_area_by_state if x[0] == state
            ][0]
            state_arable_area = [x[1]
                                 for x in arable_area_by_state if x[0] == state][0]
            state_plantations_total = [
                state_plantations_total
                for st, state_plantations_total in plantations_by_state
                if st == state
            ][0]
            state_statistics[state] = {
                "state": state,
                "farms_total": state_amount,
                "farms_percent": self.get_percent(total_farms, state_amount),
                "plantation_statistics": {
                    "state_total": state_plantations_total,
                    "percent": self.get_percent(
                        total_plantations, state_plantations_total
                    ),
                },
                "ground_use_statistics": {
                    "total_area": state_total_area or 0,
                    "vegetation_area_total": state_vegetation_area or 0,
                    "vegetation_area_percent": self.get_percent(
                        state_total_area, state_vegetation_area
                    ),
                    "arable_area_total": state_arable_area or 0,
                    "arable_area_percent": self.get_percent(
                        state_total_area, state_arable_area
                    ),
                },
            }

        logger.info("Estatísticas por estado calculadas com sucesso")
        return list(state_statistics.values())

    def get_plantation_statistics(self) -> list[PlantationStatistics]:
        """
        Calcula estatísticas de plantações por safra.

        Returns:
            list[PlantationStatistics]: Uma lista de dicionários contendo estatísticas de plantações
                                       por safra, incluindo o total de plantações e a porcentagem
                                       em relação ao total de plantações da safra.
        """
        logger.info("Calculando estatísticas de plantações")
        plantations_stats = self.plantation_repo.get_plantations_statistics()
        seasons_plantations_total = (
            self.plantation_repo.get_plantations_total_by_season()
        )
        output = {}
        for season_id, plantation_id, total_plantations in plantations_stats:
            if season_id not in output:
                season_plantations_total = [
                    t[1] for t in seasons_plantations_total if t[0] == season_id
                ][0]
                output[season_id] = {
                    "season_id": season_id,
                    "season_plantations_total": season_plantations_total,
                    "statistics": [],
                }
            output[season_id]["statistics"].append(
                {
                    "plantation_id": plantation_id,
                    "total_plantations": total_plantations,
                    "percent": self.get_percent(
                        season_plantations_total, total_plantations
                    ),
                }
            )

        logger.info("Estatísticas de plantações calculadas com sucesso")
        return list(output.values())

    def get_ground_use_statistics(self) -> GroundUseStatistics:
        """
        Calcula estatísticas de uso do solo, incluindo áreas de vegetação e cultivável.

        Returns:
            GroundUseStatistics: Um dicionário contendo estatísticas de uso do solo,
                                incluindo a porcentagem e o total de áreas de vegetação e cultivável.
        """
        logger.info("Calculando estatísticas de uso do solo")
        total_area = self.farm_repo.get_total_area()
        vegetation_area = self.farm_repo.get_total_vegetation_area()
        arable_area = self.farm_repo.get_total_arable_area()

        ground_use_stats = {
            "vegetation_area_percent": self.get_percent(total_area, vegetation_area),
            "vegetation_area_total": vegetation_area,
            "arable_area_percent": self.get_percent(total_area, arable_area),
            "arable_area_total": arable_area,
            "total_area": total_area,
        }

        logger.info("Estatísticas de uso do solo calculadas com sucesso")
        return ground_use_stats
