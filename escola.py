from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SalaDeAula:
    identificacao: str
    capacidade: int
    ativa: bool = True

    def desativar(self) -> None:
        self.ativa = False

    def abrir(self) -> None:
        self.ativa = True


@dataclass
class Professor:
    nome: str
    registro_profissional: str
    escolas: list[Escola] = field(default_factory=list, repr=False)

    def vincular_escola(self, escola: Escola) -> None:
        if escola not in self.escolas:
            self.escolas.append(escola)
        if self not in escola.professores:
            escola.professores.append(self)

    def desvincular_escola(self, escola: Escola) -> None:
        if escola in self.escolas:
            self.escolas.remove(escola)
        if self in escola.professores:
            escola.professores.remove(self)


@dataclass
class Endereco:
    logradouro: str
    numero: str
    cidade: str
    cep: str

    def atualizar(self, logradouro: str, numero: str, cidade: str, cep: str) -> None:
        self.logradouro = logradouro
        self.numero = numero
        self.cidade = cidade
        self.cep = cep


@dataclass
class Aluno:
    nome: str
    matricula: str
    endereco: Endereco

    def atualizar_endereco(self, endereco: Endereco) -> Endereco:
        endereco_anterior = self.endereco
        self.endereco = endereco
        return endereco_anterior

    def remover(self) -> Endereco:
        return self.endereco


@dataclass
class Escola:
    nome: str
    endereco: str
    salas: list[SalaDeAula] = field(default_factory=list)
    professores: list[Professor] = field(default_factory=list, repr=False)
    ativa: bool = True

    def adicionar_sala(self, identificacao: str, capacidade: int) -> SalaDeAula:
        if not self.ativa:
            raise ValueError("Não é possível adicionar sala a uma escola encerrada.")
        sala = SalaDeAula(identificacao, capacidade)
        self.salas.append(sala)
        return sala

    def vincular_professor(self, professor: Professor) -> None:
        professor.vincular_escola(self)

    def desvincular_professor(self, professor: Professor) -> None:
        professor.desvincular_escola(self)

    def encerrar(self) -> None:
        for sala in self.salas:
            sala.desativar()
        self.salas.clear()
        for professor in self.professores.copy():
            self.desvincular_professor(professor)
        self.ativa = False


def exemplo() -> None:
    escola = Escola("Escola Horizonte", "Rua das Flores, 100")
    escola.adicionar_sala("Sala 1", 30)

    professora = Professor("Ana Souza", "PROF-123")
    professora.vincular_escola(escola)

    endereco = Endereco("Rua Central", "42", "Recife", "50000-000")
    aluno = Aluno("Caio Lima", "2026-001", endereco)
    endereco_preservado = aluno.remover()

    outro_aluno = Aluno("Lia Alves", "2026-002", endereco_preservado)
    assert outro_aluno.endereco is endereco

    escola.encerrar()
    assert not escola.salas
    assert not escola.ativa
    assert not professora.escolas
    print("Exemplo executado: endereço preservado e escola encerrada.")


if __name__ == "__main__":
    exemplo()
