class Canal:
    """Representa os dados básicos de um canal de navegação."""

    def __init__(
        self,
        largura: float,
        profundidade: float,
        comprimento: float,
    ) -> None:
        self.largura = largura
        self.profundidade = profundidade
        self.comprimento = comprimento

    def __str__(self) -> str:
        return (
            f"Canal: largura={self.largura} m, profundidade={self.profundidade} m, "
            f"comprimento={self.comprimento} m"
    )