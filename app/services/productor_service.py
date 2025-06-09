from fastapi import HTTPException
from sqlalchemy.orm import Session
from validate_docbr import CNPJ, CPF

from app.core.logger import logger
from app.db.repositories.productor_repository import ProductorRepository
from app.schemas.farm import Farm
from app.schemas.productor import ProductorCreate


class ProductorService:
    def __init__(self, db: Session):
        self.db = db
        self.productor_repo = ProductorRepository(db)

    def validate_cpf_cnpj(self, cpf_cnpj):
        """
        Valida se o CPF ou CNPJ é válido.

        Args:
            cpf_cnpj (str): CPF ou CNPJ a ser validado.

        Returns:
            bool: True se o CPF/CNPJ for válido, False caso contrário.
        """
        check_cnpj = CNPJ()
        check_cpf = CPF()
        if check_cnpj.validate(cpf_cnpj):
            logger.info(f"CNPJ válido: {cpf_cnpj}")
            return True
        elif check_cpf.validate(cpf_cnpj):
            logger.info(f"CPF válido: {cpf_cnpj}")
            return True
        else:
            logger.error(f"CPF/CNPJ inválido: {cpf_cnpj}")
            return False

    def create_productor(self, productor: ProductorCreate):
        """
        Cria um novo produtor.

        Args:
            productor (ProductorCreate): Dados do produtor a ser criado.

        Returns:
            Productor: O produtor criado.

        Raises:
            HTTPException: Se o CPF/CNPJ for inválido ou já estiver cadastrado.
        """
        logger.info(
            f"Tentando criar produtor com CPF/CNPJ: {productor.cpf_cnpj}")
        if not self.validate_cpf_cnpj(productor.cpf_cnpj):
            logger.error(
                f"Falha ao criar produtor: CPF/CNPJ inválido: {productor.cpf_cnpj}"
            )
            raise HTTPException(status_code=400, detail="CPF/CNPJ inválido")
        if self.productor_repo.get_productor_by_cpf_cnpj(productor.cpf_cnpj):
            logger.error(
                f"Falha ao criar produtor: CPF/CNPJ já cadastrado: {productor.cpf_cnpj}"
            )
            raise HTTPException(
                status_code=400,
                detail="CPF/CNPJ já cadastrado")

        created_productor = self.productor_repo.create_productor(productor)
        logger.info(f"Produtor criado com sucesso: {created_productor.id}")
        return created_productor

    def get_productor_by_id(self, productor_id: int):
        """
        Busca um produtor pelo seu ID.

        Args:
            productor_id (int): ID do produtor a ser buscado.

        Returns:
            Productor: O produtor encontrado.

        Raises:
            HTTPException: Se o produtor não for encontrado.
        """
        logger.info(f"Buscando produtor por ID: {productor_id}")
        productor = self.productor_repo.get_productor_by_id(productor_id)
        if not productor:
            logger.error(f"Produtor não encontrado: {productor_id}")
            raise HTTPException(status_code=404, detail="Productor not found")
        logger.info(f"Produtor encontrado: {productor_id}")
        return productor

    def list_productors(self, offset: int = 0, limit: int = 100):
        """
        Lista todos os produtores com paginação.

        Args:
            offset (int): Número de registros a serem pulados (padrão: 0).
            limit (int): Número máximo de registros a serem retornados (padrão: 100).

        Returns:
            list[Productor]: Lista de produtores.
        """
        logger.info(
            f"Listando produtores com offset: {offset} e limite: {limit}")
        productors = self.productor_repo.list_productors(
            offset=offset, limit=limit)
        logger.info(f"Total de produtores listados: {len(productors)}")
        return productors

    def update_productor(self, productor_id: int, productor: ProductorCreate):
        """
        Atualiza um produtor existente.

        Args:
            productor_id (int): ID do produtor a ser atualizado.
            productor (ProductorCreate): Novos dados do produtor.

        Returns:
            Productor: O produtor atualizado.

        Raises:
            HTTPException: Se o CPF/CNPJ for inválido ou o produtor não for encontrado.
        """
        logger.info(f"Tentando atualizar produtor: {productor_id}")
        if not self.validate_cpf_cnpj(productor.cpf_cnpj):
            logger.error(
                f"Falha ao atualizar produtor: CPF/CNPJ inválido: {productor.cpf_cnpj}"
            )
            raise HTTPException(status_code=400, detail="CPF/CNPJ inválido")
        updated_productor = self.productor_repo.update_productor(
            productor_id, productor
        )
        if not updated_productor:
            logger.error(
                f"Falha ao atualizar produtor: Produtor não encontrado: {productor_id}"
            )
            raise HTTPException(status_code=404, detail="Productor not found")
        logger.info(f"Produtor atualizado com sucesso: {productor_id}")
        return updated_productor

    def delete_productor(self, productor_id: int):
        """
        Remove um produtor existente.

        Args:
            productor_id (int): ID do produtor a ser removido.

        Returns:
            Productor: O produtor removido.

        Raises:
            HTTPException: Se o produtor não for encontrado ou se houver fazendas relacionadas.
        """
        logger.info(f"Tentando deletar produtor: {productor_id}")
        productor = self.productor_repo.get_productor_by_id(productor_id)
        if not productor:
            logger.error(
                f"Falha ao deletar produtor: Produtor não encontrado: {productor_id}"
            )
            raise HTTPException(status_code=404, detail="Productor not found")
        if productor.farms:
            logger.error(
                f"Falha ao deletar produtor: Produtor possui fazendas relacionadas: {productor_id}"
            )
            raise HTTPException(
                status_code=400,
                detail="Cannot delete productor because it has related records",
            )

        deleted_productor = self.productor_repo.remove_productor(productor_id)
        if not deleted_productor:
            logger.error(
                f"Falha ao deletar produtor: Produtor não encontrado: {productor_id}"
            )
            raise HTTPException(status_code=404, detail="Productor not found")
        logger.info(f"Produtor deletado com sucesso: {productor_id}")
        return deleted_productor

    def get_productor_farms(self, productor_id: int) -> list[Farm]:
        """
        Busca as fazendas associadas a um produtor.

        Args:
            productor_id (int): ID do produtor.

        Returns:
            list[Farm]: Lista de fazendas associadas ao produtor.

        Raises:
            HTTPException: Se o produtor não for encontrado.
        """
        logger.info(f"Buscando fazendas do produtor: {productor_id}")
        productor = self.productor_repo.get_productor_by_id(productor_id)
        if not productor:
            logger.error(
                f"Falha ao buscar fazendas: Produtor não encontrado: {productor_id}"
            )
            raise HTTPException(status_code=404, detail="Productor not found")
        logger.info(f"Fazendas encontradas para o produtor: {productor_id}")
        return productor.farms
