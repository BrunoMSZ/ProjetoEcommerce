class Endereco:
    def __init__(self: object, rua: str, numero: int, cidade: str, estado: str, cep: str, pais: str, idCadastroCliente: int) -> None:
        self.__id: int = id
        self.__rua: str = rua
        self.__numero: int = numero
        self.__cidade: str = cidade
        self.__estado: str = estado
        self.__cep: str = cep
        self.__pais: str = pais
        self.__idCadastroCliente: int = idCadastroCliente

    @property
    def id(self):
        return self.__id
    
    @property
    def rua(self):
        return self.__rua
    
    @property
    def numero(self):
        return self.__numero

    @property
    def cidade(self):
        return self.__cidade
    
    @property
    def estado(self):
        return self.__estado
    @property
    def cep(self):
        return self.__cep

    @property
    def pais(self):
        return self.__pais
    
    @property
    def idCadastroCliente(self):
        return self.__idCadastroCliente


class Telefone:
    def __init__(self: object, numero: str, idCadastroCliente: int) -> None:
        self.__id: int = id
        self.__numero: str = numero
        self.__idCadastroCliente: int = idCadastroCliente

    @property
    def id(self):
        return self.__id
    
    @property
    def numero(self):
        return self.__numero

    @property
    def idCadastroCliente(self):
        return self.__idCadastroCliente


class Produto:
    def __init__(self: object, nome: str, descricao: str, preco: float, estoque: int, idCategoria: int, idItemPedido: int, cor: str, voltagem: str, comentario:str, dimensao: str) -> None:
        self.__id: int = id
        self.__nome: str = nome
        self.__descricao: str = descricao
        self.__preco: float = preco
        self.__estoque: int = estoque
        self.__idCategoria: int = idCategoria
        self.__idItemPedido: str = idItemPedido
        self.__cor: str = cor
        self.__voltagem: str = voltagem
        self.__comentario: str = comentario
        self.__dimensao: str = dimensao

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def descricao(self):
        return self.__descricao

    @property
    def preco(self):
        return self.__preco
    
    @property
    def estoque(self):
        return self.__estoque
    @property
    def idCategoria(self):
        return self.__idCategoria

    @property
    def idItemPedido(self):
        return self.__idItemPedido
    
    @property
    def cor(self):
        return self.__cor
    
    @property
    def voltagem(self):
        return self.__voltagem

    @property
    def comentario(self):
        return self.__comentario

    @property
    def dimensao(self):
        return self.__dimensao


class ItemPedido:
    def __init__(self: object, quantidade: int, precoTotal: float, idPedido: int, desconto: str) -> None:
        self.__id: int = id
        self.__quantidade: int = quantidade
        self.__precoTotal: float = precoTotal
        self.__idPedido: str = idPedido
        self.__desconto: str = desconto

    @property
    def id(self):
        return self.__id
    
    @property
    def quantidade(self):
        return self.__quantidade
    
    @property
    def precoTotal(self):
        return self.__precoTotal

    @property
    def idPedido(self):
        return self.__idPedido
    
    @property
    def desconto(self):
        return self.__desconto



