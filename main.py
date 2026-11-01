from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Configuração do banco de dados
engine = create_engine("sqlite:///clientes.db", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# Modelo Cliente
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    enderecos = relationship(
        "Endereco",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )


# Modelo Endereco
class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rua = Column(String(150), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="enderecos")


Base.metadata.create_all(engine)


# CREATE - Cadastrar cliente e endereço
def criar_cliente():
    nome = input("Nome: ")
    email = input("E-mail: ")
    rua = input("Rua: ")
    cidade = input("Cidade: ")
    estado = input("Estado (UF): ").upper()

    if not all([nome.strip(), email.strip(), rua.strip(),
                cidade.strip(), estado.strip()]):
        print("Todos os campos são obrigatórios.")
        return

    try:
        with SessionLocal() as session:
            cliente = Cliente(
                nome=nome,
                email=email,
                enderecos=[
                    Endereco(
                        rua=rua,
                        cidade=cidade,
                        estado=estado
                    )
                ]
            )

            session.add(cliente)
            session.commit()

            print("Cliente cadastrado com sucesso!")

    except IntegrityError:
        print("Este e-mail já está cadastrado.")


# READ - Listar clientes e endereços
def listar_clientes():
    with SessionLocal() as session:
        clientes = session.query(Cliente).all()

        if not clientes:
            print("Nenhum cliente cadastrado.")
            return

        for cliente in clientes:
            print(f"\nID: {cliente.id}")
            print(f"Nome: {cliente.nome}")
            print(f"E-mail: {cliente.email}")

            if not cliente.enderecos:
                print("Nenhum endereço cadastrado.")

            for endereco in cliente.enderecos:
                print(
                    f"Endereço ID: {endereco.id} | "
                    f"{endereco.rua}, {endereco.cidade} - "
                    f"{endereco.estado}"
                )


# UPDATE - Atualizar cliente
def atualizar_cliente():
    try:
        id_cliente = int(input("ID do cliente: "))

        with SessionLocal() as session:
            cliente = session.get(Cliente, id_cliente)

            if cliente is None:
                print("Cliente não encontrado.")
                return

            nome = input("Novo nome: ")
            email = input("Novo e-mail: ")

            if not nome.strip() or not email.strip():
                print("Os campos não podem ficar vazios.")
                return

            cliente.nome = nome
            cliente.email = email

            session.commit()
            print("Cliente atualizado com sucesso!")

    except ValueError:
        print("Informe um ID válido.")
    except IntegrityError:
        print("Este e-mail já está cadastrado.")


# DELETE - Excluir cliente e seus endereços
def excluir_cliente():
    try:
        id_cliente = int(input("ID do cliente: "))

        with SessionLocal() as session:
            cliente = session.get(Cliente, id_cliente)

            if cliente is None:
                print("Cliente não encontrado.")
                return

            session.delete(cliente)
            session.commit()

            print("Cliente e seus endereços excluídos!")

    except ValueError:
        print("Informe um ID válido.")


# CREATE - Adicionar endereço a um cliente existente
def adicionar_endereco():
    try:
        id_cliente = int(input("ID do cliente: "))

        with SessionLocal() as session:
            cliente = session.get(Cliente, id_cliente)

            if cliente is None:
                print("Cliente não encontrado.")
                return

            rua = input("Rua: ")
            cidade = input("Cidade: ")
            estado = input("Estado (UF): ").upper()

            if not all([rua.strip(), cidade.strip(), estado.strip()]):
                print("Todos os campos são obrigatórios.")
                return

            endereco = Endereco(
                rua=rua,
                cidade=cidade,
                estado=estado,
                cliente_id=id_cliente
            )

            session.add(endereco)
            session.commit()

            print("Endereço cadastrado com sucesso!")

    except ValueError:
        print("Informe um ID válido.")


# UPDATE - Atualizar endereço
def atualizar_endereco():
    try:
        id_endereco = int(input("ID do endereço: "))

        with SessionLocal() as session:
            endereco = session.get(Endereco, id_endereco)

            if endereco is None:
                print("Endereço não encontrado.")
                return

            endereco.rua = input("Nova rua: ")
            endereco.cidade = input("Nova cidade: ")
            endereco.estado = input("Novo estado (UF): ").upper()

            session.commit()
            print("Endereço atualizado com sucesso!")

    except ValueError:
        print("Informe um ID válido.")


# DELETE - Excluir endereço
def excluir_endereco():
    try:
        id_endereco = int(input("ID do endereço: "))

        with SessionLocal() as session:
            endereco = session.get(Endereco, id_endereco)

            if endereco is None:
                print("Endereço não encontrado.")
                return

            session.delete(endereco)
            session.commit()

            print("Endereço excluído com sucesso!")

    except ValueError:
        print("Informe um ID válido.")


# JOIN - Consultar clientes e seus endereços
def consultar_join():
    with SessionLocal() as session:
        resultados = (
            session.query(Cliente, Endereco)
            .join(Endereco, Cliente.id == Endereco.cliente_id)
            .all()
        )

        if not resultados:
            print("Nenhum cliente com endereço encontrado.")
            return

        print("\n===== CLIENTES E ENDEREÇOS =====")

        for cliente, endereco in resultados:
            print(f"\nCliente: {cliente.nome}")
            print(f"E-mail: {cliente.email}")
            print(f"Endereço: {endereco.rua}")
            print(f"Cidade: {endereco.cidade}")
            print(f"Estado: {endereco.estado}")


# Menu principal
def menu():
    while True:
        print("\n===== SISTEMA DE GERENCIAMENTO =====")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("5 - Consultar clientes e endereços (JOIN)")
        print("6 - Adicionar endereço")
        print("7 - Atualizar endereço")
        print("8 - Excluir endereço")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            if opcao == "1":
                criar_cliente()
            elif opcao == "2":
                listar_clientes()
            elif opcao == "3":
                atualizar_cliente()
            elif opcao == "4":
                excluir_cliente()
            elif opcao == "5":
                consultar_join()
            elif opcao == "6":
                adicionar_endereco()
            elif opcao == "7":
                atualizar_endereco()
            elif opcao == "8":
                excluir_endereco()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida.")

        except Exception as erro:
            print(f"Erro ao executar operação: {erro}")


if __name__ == "__main__":
    menu()
