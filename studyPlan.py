import this
from copy import copy


class subject:
    correlativas = []
    id = 0
    nombre = "Default"
    def __init__(self,id,nombre):
        self.correlativas = []
        self.id = id
        self.nombre = nombre
    def addCorrelativa(self,subj: 'subject'):
        self.correlativas.append(copy(subj))
    def __str__(self):

        return f"id = {self.id}, nombre = {self.nombre}, correlativas = {self.correlativas}"


class studyPlan:
    nombre = "Ingenieria de sistemas"
    id = 2011
    materias = []
    materias_copia = []

    def __init__(self,nombre = "Ingenieria de Sistemas",id = 2011):
        self.nombre = nombre
        self.id = id


    def addSubject(self,subj: subject):
        self.materias.append(subj)
        self.materias_copia.append(copy(subj))

    def getSubjectbyName(self,name):
        for m in self.materias_copia:
            if m.nombre == name:
                return m
    def getSubject(self,id):
        for m in self.materias_copia:
            if m.id == id:
                materia = subject(m.id, m.nombre)
                return materia

    def asignarCorrelativa(self):
        for a in self.materias:
            if a.id == 1:  # prog1
                a.addCorrelativa(self.getSubject(5))
            elif a.id == 2:  # analisis1
                a.addCorrelativa(self.getSubject(7))
                a.addCorrelativa(self.getSubject(11))
            elif a.id == 145:  # algebra1
                a.addCorrelativa(self.getSubject(125))
                a.addCorrelativa(self.getSubject(127))
            elif a.id == 4:  # ciencias1
                a.addCorrelativa(self.getSubject(8))
                a.addCorrelativa(self.getSubject(9))
            elif a.id == 5:  # prog2
                a.addCorrelativa(self.getSubject(9))
                a.addCorrelativa(self.getSubject(8))
                a.addCorrelativa(self.getSubject(10))
            elif a.id == 7:  # fisica
                a.addCorrelativa(self.getSubject(12))
            elif a.id == 125:  # lineal
                a.addCorrelativa(self.getSubject(15))
            elif a.id == 127:  # discreta
                a.addCorrelativa(self.getSubject(9))
                a.addCorrelativa(self.getSubject(8))
            elif a.id == 8:  # ciencias2
                a.addCorrelativa(self.getSubject(13))
            elif a.id == 9:  # ayda1
                a.addCorrelativa(self.getSubject(13))
            elif a.id == 10:  # introarqui
                a.addCorrelativa(self.getSubject(14))
            elif a.id == 11:  # analisis2
                a.addCorrelativa(self.getSubject(15))
                a.addCorrelativa(self.getSubject(30))
            elif a.id == 12:  # eym
                a.addCorrelativa(self.getSubject(16))
            elif a.id == 13:  # ayda2
                a.addCorrelativa(self.getSubject(22))
                a.addCorrelativa(self.getSubject(19))
                a.addCorrelativa(self.getSubject(20))
            elif a.id == 14:  # comu1
                a.addCorrelativa(self.getSubject(28))
                a.addCorrelativa(self.getSubject(29))
            elif a.id == 15:  # proba
                a.addCorrelativa(self.getSubject(19))
            elif a.id == 16:  # electronica
                a.addCorrelativa(self.getSubject(21))
            elif a.id == 19:  # estructuradatos
                a.addCorrelativa(self.getSubject(23))
                a.addCorrelativa(self.getSubject(25))
            elif a.id == 20:  # meto
                a.addCorrelativa(self.getSubject(23))
            elif a.id == 21:  # arqui1
                a.addCorrelativa(self.getSubject(25))
            elif a.id == 22:  # objetos
                a.addCorrelativa(self.getSubject(24))
            elif a.id == 23:  # basedatos
                a.addCorrelativa(self.getSubject(31))
            elif a.id == 24:  # lenguajes
                a.addCorrelativa(self.getSubject(32))
            elif a.id == 25:  # sisop
                a.addCorrelativa(self.getSubject(29))
            elif a.id == 31:  # diseñosoftware
                a.addCorrelativa(self.getSubject(33))


    def __str__(self):
        materias = ""
        for m in self.materias:
            materias += str(m)
        return f"nombre = {self.nombre}, id = {self.id}, materias = {materias}"