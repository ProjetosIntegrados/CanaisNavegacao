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