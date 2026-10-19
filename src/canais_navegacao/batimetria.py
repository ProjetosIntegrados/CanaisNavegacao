class PontoBatimetrico:
    """Representa um ponto de uma seção batimétrica."""

    def __init__(
        self,
        offset: float,
        profundidade: float,
    ) -> None:
        self.offset = offset
        self.profundidade = profundidade


class SecaoBatimetrica:
    """Representa uma seção transversal com seus pontos batimétricos."""

    def __init__(
        self,
        identificacao: str,
        distancia: float,
        pontos: list[PontoBatimetrico],
    ) -> None:
        self.identificacao = identificacao
        self.distancia = distancia
        self.pontos = pontos
                