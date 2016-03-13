# -*- coding: utf-8 -*-
from itertools import chain
from atores import ATIVO


VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)


class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []


    def adicionar_obstaculo(self, *obstaculos):
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """
        self._obstaculos.extend(obstaculos)

    def adicionar_porco(self, *porcos):
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        self._porcos.extend(porcos)

    def adicionar_passaro(self, *passaros):
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        self._passaros.extend(passaros)

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """

        haveBird = self._existe_passaro_ativo()
        havePig = self._existe_porco_ativo()
        if (not haveBird) and havePig:
            return DERROTA
        elif haveBird and havePig:
            return EM_ANDAMENTO
        else:
            return  VITORIA

    def lancar(self, angulo, tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """
        passaro = self._passaro_parado()

        if passaro:
            passaro.lancar(angulo, tempo)



    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """
        pontos=[]

        for ator in chain(self._passaros, self._obstaculos, self._porcos) :
            x, y =  ator.calcular_posicao(tempo)
            pontos.append( Ponto(x,y, ator.caracter()))

        self._check_colisao()

        return pontos

    def _check_colisao(self):
        for passaro in self._passaros:

            if not passaro.estaAtivo():
                continue

            passaro.colidir_com_chao()
            for ator in chain(self._obstaculos, self._porcos):
                passaro.colidir(ator , self.intervalo_de_colisao)

    def _passaro_parado(self):
        for p in self._passaros:
            if not p.foi_lancado():
                return p
        return False

    def _transformar_em_ponto(self, ator):
        return Ponto(ator.x, ator.y, ator.caracter())

    def _existe_porco_ativo(self):
        return self._verificar_se_existe_ator_ativo(self._porcos)

    def _existe_passaro_ativo(self):
        return self._verificar_se_existe_ator_ativo(self._passaros)

    def _verificar_se_existe_ator_ativo(self, atores):
        for a in atores:
            if a.status == ATIVO:
                return True
        return False



