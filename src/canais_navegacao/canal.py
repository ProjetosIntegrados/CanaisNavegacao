class Canal:
    """Representa os dados básicos de um canal de navegação."""

    def __init__(
        self,
        profundidade: float,
        comprimento: float,
        tipo: str,
        largura: float | None = None,
        talude: float | None = None,
        altura_calha: float | None = None,
    ) -> None:
        self.largura = largura
        self.talude = talude
        self.altura_calha = altura_calha
        self.profundidade = profundidade
        self.comprimento = comprimento
        if tipo not in ("U", "R", "C"):            
           raise ValueError("Tipo de canal deve ser U, R ou C.")
        
        if tipo == "R" and (
           largura is None or talude is None or altura_calha is None
        ):
           raise ValueError(
            "Canal R requer largura, talude e altura da calha."
    )
        if tipo == "C" and (
           largura is None or talude is None
        ):
           raise ValueError(
            "Canal C requer largura e talude."
    )
        self.tipo = tipo

    def __str__(self) -> str:
        return (
            f"Canal: largura={self.largura} m, profundidade={self.profundidade} m, "
            f"comprimento={self.comprimento} m, tipo={self.tipo}"
    )