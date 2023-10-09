import FreeCAD, FreeCADGui, Part, math, os


path_ui = str(os.path.dirname(__file__))+'/EscadaGui.ui'


class EscadaPainel:
	def __init__(self):
		# Carrega a GUI
		self.form = FreeCADGui.PySideUic.loadUi(path_ui)

		#define a função do botão calcular
		self.form.btn_calcular.clicked.connect(self.calc)

	def calc(self):
		#função executada quando o botão calcular é clicado
		#calcula os espelhos e pisos da escada segundo a equação de Blondel
		
		print(self.form.Altura.value())
		espelho = float(self.form.Altura.value())/float(self.form.NDegraus.value())
		piso = 64 - (2 * espelho)

		self.form.Espelho.setValue(espelho)
		self.form.Piso.setValue(piso)  

	def accept(self):
		#Função executada quando o botão ok for clicado
		#cria o objeto Escada

		obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Escada')
		Escada(obj,self.form.TipoEscada.currentText(),self.form.Patamar.currentText(),self.form.TipoDegrau.currentText(),
			self.form.TipoLongarina.currentText(), self.form.EspecuraEstrutura.value(),self.form.LarguraLongarina.value(),
			self.form.Altura.value(),self.form.Largura.value(),self.form.NDegraus.value(),self.form.EspecuraDegrau.value(),
			self.form.Espelho.value(),self.form.Piso.value(),self.form.DistLances.value(),self.form.Mastro.currentText(),
			self.form.DiametroEspiral.value(),self.form.LarguraPatamar.value())
		obj.ViewObject.Proxy = 0

		if self.form.TipoLongarina.currentText() != 'Nenhum':
			obj2 = FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Longarina')
			Longarina(obj2,self.form.TipoEscada.currentText(),self.form.Patamar.currentText(),self.form.TipoDegrau.currentText(),
				self.form.TipoLongarina.currentText(), self.form.EspecuraEstrutura.value(),self.form.LarguraLongarina.value(),
				self.form.Altura.value(),self.form.Largura.value(),self.form.NDegraus.value(),self.form.EspecuraDegrau.value(),
				self.form.Espelho.value(),self.form.Piso.value(),self.form.DistLances.value(),self.form.Mastro.currentText(),
				self.form.DiametroEspiral.value(),self.form.LarguraPatamar.value(),obj)
			obj2.ViewObject.Proxy = 0



		FreeCAD.ActiveDocument.recompute()


class Escada:
	def __init__(self, obj,tipoescada,patamar,tipodegrau,tipolongarina,especuraestrutura,
		larguralongarina,altura,largura,ndegraus,especuradegrau,espelho,piso,distlances,mastro,diametroespiral,largurapatamar):
		obj.Proxy = self

		#Design
		obj.addProperty("App::PropertyEnumeration", "TipoEscada","Design","Tipo de escada")
		obj.TipoEscada = ['Escada reta','Escada L', 'Escada U','Escada espiral']
		obj.TipoEscada = tipoescada

		obj.addProperty("App::PropertyEnumeration", "Patamar","Design","Adiciona um patamar ao lance de escada")
		obj.Patamar = ['Não','Sim']
		obj.Patamar = patamar

		obj.addProperty("App::PropertyEnumeration", "TipoDegrau","Design","Tipo de degrau")
		obj.TipoDegrau = ['Comum fechada','Comum aberta', 'Vazada','Plissada']
		obj.TipoDegrau = tipodegrau



		#Estrutura

		'''obj.addProperty("App::PropertyEnumeration", "TipoLongarina","Estrutura","Posição da longarina")
		obj.TipoLongarina = ['Nenhum','Central','Borda', 'Lateral']
		obj.TipoLongarina = tipolongarina'''

		obj.addProperty("App::PropertyLength", "EspecuraEstrutura","Estrutura","Espeçura da estrutura maçiça os longarinas")
		obj.EspecuraEstrutura = especuraestrutura * 10

		'''obj.addProperty("App::PropertyLength", "LarguraLongarina","Estrutura","Largura da longarina")
		obj.LarguraLongarina = larguralongarina * 10'''

		'''obj.addProperty("App::PropertyEnumeration", "Mastro","Estrutura","Posição da longarina")
		obj.Mastro = ['Não','Sim']
		obj.Mastro = mastro'''

		

		#Dimençoes
		obj.addProperty("App::PropertyLength", "Altura","Dimensoes","Altura do desnível a vencer com a escada")
		obj.Altura = altura * 10

		obj.addProperty("App::PropertyLength", "Largura","Dimensoes","Largura dos lances da escada")
		obj.Largura = largura * 10

		obj.addProperty("App::PropertyInteger", "NDegraus","Dimensoes","Número de degraus da escada")
		obj.NDegraus = ndegraus 

		obj.addProperty("App::PropertyLength", "EspecuraDegrau","Dimensoes","Espeçura dos degraus da escada")
		obj.EspecuraDegrau = especuradegrau * 10

		obj.addProperty("App::PropertyLength", "Espelho","Dimensoes","Altura dos espelhos da escada")
		obj.Espelho = espelho * 10

		obj.addProperty("App::PropertyLength", "Piso","Dimensoes","Largura do piso dos degraus da escada")
		obj.Piso = piso * 10

		obj.addProperty("App::PropertyLength", "DistLances","Dimensoes","Distanci entre os lances de escada (Parar formato U)")
		obj.DistLances = distlances * 10

		obj.addProperty("App::PropertyLength", "DiametroEspiral","Dimensoes","Diametro interno da espiral da escada)")
		obj.DiametroEspiral = diametroespiral * 10

		obj.addProperty("App::PropertyLength", "LarguraPatamar","Dimensoes","Largura do patamar da escada")
		obj.LarguraPatamar = largurapatamar * 10




	def execute(self,obj):

		#Verifica se as dimençoes essenciais não estão zeradas
		if obj.Altura == 0 or obj.Largura == 0 or obj.NDegraus == 0 :
			return

		#Se as dimençoes do espelho e piso não forem definidas ambos são calculados automaticamente
		'''if obj.Espelho == 0 and obj.Piso !=0:
			obj.Espelho = obj.Altura/obj.NDegraus

		elif obj.Espelho != 0 and obj.Piso == 0:
			obj.NDegraus = int(obj.Altura/obj.Espelho)
			obj.Piso = 64 - (2 * obj.Espelho)

		elif obj.Espelho == 0 and obj. Piso == 0:
			obj.Espelho = obj.Altura/obj.NDegraus
			obj.Piso = float(64 - (2 * obj.Espelho))

		'''
		'''if obj.Espelho != 0 and obj.Piso != 0:
			obj.NDegraus = int(obj.Altura/obj.Espelho)'''

		


		#verifica se a largura do patamar foi definida
		if obj.LarguraPatamar == 0:
			obj.LarguraPatamar = obj.Largura



		n_degraus_lances = []
		# calcula o numero de degraus de cada lance da escada
		if obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não':
			n_degraus_lances.append(obj.NDegraus)

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim':
			n_degraus_lances.append(math.ceil((obj.NDegraus-1)/2))
			n_degraus_lances.append(math.floor((obj.NDegraus-1)/2))

		elif obj.TipoEscada == 'Escada L' and  obj.Patamar == 'Sim':
			n_degraus_lances.append(math.ceil((obj.NDegraus-1)/2))
			n_degraus_lances.append(math.floor((obj.NDegraus-1)/2))

		elif obj.TipoEscada == 'Escada L' and  obj.Patamar == 'Não':
			n_degraus_lances.append(math.ceil((obj.NDegraus-3)/2))
			n_degraus_lances.append(math.floor((obj.NDegraus-3)/2))

		elif obj.TipoEscada == 'Escada U' and  obj.Patamar == 'Sim' and obj.DistLances < obj.Piso:
			n_degraus_lances.append(math.ceil((obj.NDegraus-1)/2))
			n_degraus_lances.append(0)
			n_degraus_lances.append(math.floor((obj.NDegraus-1)/2))

		elif obj.TipoEscada == 'Escada U' and  obj.Patamar == 'Não' and obj.DistLances < obj.Piso:
			n_degraus_lances.append(math.ceil((obj.NDegraus-6)/2))
			n_degraus_lances.append(0)
			n_degraus_lances.append(math.floor((obj.NDegraus-6)/2))

		elif obj.TipoEscada == 'Escada U' and  obj.Patamar == 'Sim' and obj.DistLances >= obj.Piso:
			degraus_intermediario = math.floor(obj.DistLances/obj.Piso) # calculo do numero de degraus do lance intermediário

			n_degraus_lances.append(math.ceil((obj.NDegraus-degraus_intermediario-2)/2))
			n_degraus_lances.append(degraus_intermediario)
			n_degraus_lances.append(math.floor((obj.NDegraus-degraus_intermediario-2)/2))

		elif obj.TipoEscada == 'Escada U' and  obj.Patamar == 'Não' and obj.DistLances >= obj.Piso:
			degraus_intermediario = math.floor(obj.DistLances/obj.Piso) # calculo do numero de degraus do lance intermediário

			n_degraus_lances.append(math.ceil((obj.NDegraus-degraus_intermediario-6)/2))
			n_degraus_lances.append(degraus_intermediario)
			n_degraus_lances.append(math.floor((obj.NDegraus-degraus_intermediario-6)/2))

		elif obj.TipoEscada == 'Escada espiral':
			n_degraus_lances.append(obj.NDegraus)



		Perfil = [] #lista com as linhas dos peris dos lances da  escada
		 # lista que armazena temporariamente os seguimentos de linha dos lances

		Patamar = []

		#Gera a linha dos pisos da escada #######################################################
		if obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não':
			
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim':
			#lance 1
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)
			#lance 2
			lance = []
			for i in range(1,n_degraus_lances[1] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

		elif obj.TipoEscada == "Escada L" and obj.Patamar == 'Sim':
			#lance 1
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

			#lance 2-teste
			lance = []
			for i in range(1,n_degraus_lances[1] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

		elif obj.TipoEscada == "Escada L" and obj.Patamar == 'Não':
			#lance 1
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)
			#lance 2
			lance = []
			for i in range(1,n_degraus_lances[1] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

		elif obj.TipoEscada == "Escada U" and obj.Patamar == 'Sim':
			#lance 1
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

			#lance 2
			lance = []
			if n_degraus_lances[1] > 0: # se o numero de degraus do segundo lance da escada for maior que 0.
				
				for i in range(1,n_degraus_lances[1] + 1):
					p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
					p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
					l = Part.LineSegment(p1,p2).toShape()

					lance.append(l)

			Perfil.append(lance)

			#lance 3
			if n_degraus_lances[1] == 0: #caso o lance 2 não tenha degraus
				lance = []
				for i in range(1,n_degraus_lances[2] + 1):
					p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
					p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
					l = Part.LineSegment(p1,p2).toShape()

					lance.append(l)
				Perfil.append(lance)
			else:
				lance = []
				for i in range(1,n_degraus_lances[2] + 1):
					p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
					p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
					l = Part.LineSegment(p1,p2).toShape()

					lance.append(l)
				Perfil.append(lance)


		elif obj.TipoEscada == "Escada U" and obj.Patamar == 'Não':
			#lance 1
			lance = []
			for i in range(1,n_degraus_lances[0] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)

			Perfil.append(lance)

			#lance 2
			lance = []
			if n_degraus_lances[1] != 0: # se o numero de degraus do segundo lance da escada for maior que 0.
				
				for i in range(1,n_degraus_lances[1] + 1):
					p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
					p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
					l = Part.LineSegment(p1,p2).toShape()	

					lance.append(l)

			Perfil.append(lance)

			#lance 3
			lance = []
			for i in range(1,n_degraus_lances[2] + 1):
				p1 = FreeCAD.Vector(0,(i-1)*obj.Piso, i*obj.Espelho)
				p2 = FreeCAD.Vector(0, i*obj.Piso, i*obj.Espelho)
				l = Part.LineSegment(p1,p2).toShape()

				lance.append(l)
			Perfil.append(lance)

		
		elif obj.TipoEscada == "Escada espiral":
			#gera as faces dos degrau
			#calculo do angulo dos degraus

			ang_rad = (2*obj.Piso)/(obj.DiametroEspiral+obj.Largura)
			ang_deg = (ang_rad*180)/math.pi

			r1 = (obj.DiametroEspiral/2) #raio interno
			r2 = (obj.DiametroEspiral/2) + obj.Largura #raio externo

			#arco externo
			p1 = FreeCAD.Vector(r2*math.cos(ang_rad/2),r2*math.sin(ang_rad/2),0)
			p2 = FreeCAD.Vector(r2*math.cos(ang_rad/2),-r2*math.sin(ang_rad/2),0)
			p3 = FreeCAD.Vector(r2,0,0)

			#arco interno
			p4 = FreeCAD.Vector(r1*math.cos(ang_rad/2),r1*math.sin(ang_rad/2),0)
			p5 = FreeCAD.Vector(r1*math.cos(ang_rad/2),-r1*math.sin(ang_rad/2),0)
			p6 = FreeCAD.Vector(r1,0,0)

			#Gerando os seguimentos de linhas e arcos
			a1 = Part.Arc(p1,p3,p2).toShape()
			a2 = Part.Arc(p4,p6,p5).toShape()
			l1 = Part.LineSegment(p1,p4).toShape()
			l2 = Part.LineSegment(p2,p5).toShape()

			w = Part.Wire([a2,l1,a1,l2])
			
			#face = Part.Face(w)
			#Part.show(face)

			pisos = []
			for i in range(1,n_degraus_lances[0]+1):
				pisos.append(Part.Face(w).rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),ang_deg*i-1).translate(FreeCAD.Vector(0,0,i*obj.Espelho)))

			for i in pisos:
				Part.show(i)







		################################# Modela os lances e os patamatres das escadas ################################################

		if obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum fechada':
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)
			
			obj.Shape = solido1
			

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum fechada':
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)

			solido2 = self.lance_comum_fechada(obj,Perfil[1],(n_degraus_lances[0]+1)*obj.Espelho)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso+obj.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_fechada(obj,altura = (n_degraus_lances[0]+1)*obj.Espelho)
			solido3.translate(FreeCAD.Vector(-obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido3,solido2])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum fechada':
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)

			solido2 = self.lance_comum_fechada(obj,Perfil[1],(n_degraus_lances[0]+1)*obj.Espelho)
			solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_fechada(obj,altura = (n_degraus_lances[0]+1)*obj.Espelho)
			solido3.translate(FreeCAD.Vector(-obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido3,solido2])
			obj.Shape = solido4


		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum fechada':
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)

			solido2 = self.lance_comum_fechada(obj,Perfil[1],(n_degraus_lances[0]+3)*obj.Espelho)
			solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

			solido3 = self.degraus_fechada(obj,((n_degraus_lances[0]+1)*obj.Espelho))
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4


		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum fechada':
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_comum_fechada(obj,Perfil[1],(n_degraus_lances[0]+1)*obj.Espelho)
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido3 = self.lance_comum_fechada(obj,Perfil[2],(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho)
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido4 = self.patamar_fechada(obj,altura = (n_degraus_lances[0]+1)*obj.Espelho,comprimento = obj.LarguraPatamar)
				solido4.translate(FreeCAD.Vector(-obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.patamar_fechada(obj,altura = (n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho, comprimento = (obj.Largura + (obj.DistLances - n_degraus_lances[1]*obj.Piso)))
				solido5.translate(FreeCAD.Vector(n_degraus_lances[1]*obj.Piso,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6

			else:
				solido2 = self.lance_comum_fechada(obj,Perfil[2],(n_degraus_lances[0]+1)*obj.Espelho)
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido2.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido3 = self.patamar_fechada(obj,altura = (n_degraus_lances[0]+1)*obj.Espelho)
				solido3.translate(FreeCAD.Vector(-obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido4 = Part.Compound([solido1,solido2,solido3])
				obj.Shape = solido4

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum fechada':
			solido1 = self.lance_comum_fechada(obj,Perfil[0],0)

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_comum_fechada(obj,Perfil[1],(n_degraus_lances[0]+3)*obj.Espelho)
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

				solido3 = self.lance_comum_fechada(obj,Perfil[2],(n_degraus_lances[0]+n_degraus_lances[1]+6)*obj.Espelho)
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+6)*obj.Espelho))

				solido4 = self.degraus_fechada(obj,((n_degraus_lances[0]+1)*obj.Espelho))
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_fechada(obj,((n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho), recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_comum_fechada(obj,Perfil[2],(n_degraus_lances[0]+6)*obj.Espelho)
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+6)*obj.Espelho))

				solido4 = self.degraus_fechada(obj,((n_degraus_lances[0]+1)*obj.Espelho))
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_fechada(obj,((n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho), recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido3,solido4,solido5])
				obj.Shape = solido6




		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum aberta':###################################
			solido1 = self.lance_comum_aberta(obj,Perfil[0])
			obj.Shape = solido1

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum aberta':###################################
			solido1 = self.lance_comum_aberta(obj,Perfil[0])

			solido2 = self.lance_comum_aberta(obj,Perfil[1])
			solido2.translate(FreeCAD.Vector(0,(n_degraus_lances[0]*obj.Piso)+obj.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_aberta(obj,Perfil[0])
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum aberta':###################################
			solido1 = self.lance_comum_aberta(obj,Perfil[0])

			solido2 = self.lance_comum_aberta(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_aberta(obj,Perfil[0],comprimento = obj.Largura)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum aberta':###################################
			solido1 = self.lance_comum_aberta(obj,Perfil[0])

			solido2 = self.lance_comum_aberta(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

			solido3 = self.degraus_aberta(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2, solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Comum aberta':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_aberta(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_comum_aberta(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido3 = self.lance_comum_aberta(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido4 = self.patamar_aberta(obj,Perfil[0],comprimento = obj.Largura)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.patamar_aberta(obj,Perfil[0],comprimento = (obj.Largura),recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(n_degraus_lances[1]*obj.Piso,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_comum_aberta(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido4 = self.patamar_aberta(obj,Perfil[0],comprimento = (2*obj.Largura+obj.DistLances),recuo = True)
				solido4.translate(FreeCAD.Vector(obj.Largura+obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = Part.Compound([solido1,solido3,solido4])
				obj.Shape = solido5

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Comum aberta':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_comum_aberta(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_comum_aberta(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

				solido3 = self.lance_comum_aberta(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+6)*obj.Espelho))

				solido4 = self.degraus_aberta(obj)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_aberta(obj,recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_comum_aberta(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+6)*obj.Espelho))

				solido4 = self.degraus_aberta(obj, triangulo = False)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_aberta(obj,recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido3,solido4,solido5])
				obj.Shape = solido6





		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Vazada':###################################
			solido1 = self.lance_vazada(obj,Perfil[0])
			obj.Shape = solido1

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Vazada':###################################
			solido1 = self.lance_vazada(obj,Perfil[0])

			solido2 = self.lance_vazada(obj,Perfil[1])
			solido2.translate(FreeCAD.Vector(0,(n_degraus_lances[0]*obj.Piso)+obj.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_vazada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Vazada':###################################
			solido1 = self.lance_vazada(obj,Perfil[0])

			solido2 = self.lance_vazada(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_vazada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Vazada':###################################
			solido1 = self.lance_vazada(obj,Perfil[0])

			solido2 = self.lance_vazada(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

			solido3 = self.degraus_vazada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))


			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Vazada':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_vazada(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_vazada(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido3 = self.lance_vazada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido4 = self.patamar_vazada(obj,comprimento = obj.Largura)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.patamar_vazada(obj,comprimento = (obj.Largura + (obj.DistLances-(n_degraus_lances[1]*obj.Piso))))
				solido5.translate(FreeCAD.Vector(obj.DistLances+obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6	

			else:
				solido3 = self.lance_vazada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido4 = self.patamar_vazada(obj,comprimento = (2*obj.Largura) + obj.DistLances)
				solido4.translate(FreeCAD.Vector(obj.Largura+obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = Part.Compound([solido1,solido3,solido4])
				obj.Shape = solido5

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Vazada':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_vazada(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_vazada(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

				solido3 = self.lance_vazada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+6)*obj.Espelho))

				solido4 = self.degraus_vazada(obj)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_vazada(obj, recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3, solido4,solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_vazada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+6)*obj.Espelho))

				solido4 = self.degraus_vazada(obj)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_vazada(obj, recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso, (n_degraus_lances[0]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido3,solido4,solido5])
				obj.Shape = solido6





		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Plissada':###################################
			solido1 = self.lance_plissada(obj,Perfil[0])
			obj.Shape = solido1

		elif obj.TipoEscada == 'Escada reta' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Plissada':###################################
			solido1 = self.lance_plissada(obj,Perfil[0])

			solido2 = self.lance_plissada(obj,Perfil[1])
			solido2.translate(FreeCAD.Vector(0,(n_degraus_lances[0]*obj.Piso)+obj.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_plissada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Plissada':###################################
			solido1 = self.lance_plissada(obj,Perfil[0])

			solido2 = self.lance_plissada(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido3 = self.patamar_plissada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada L' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Plissada':###################################
			solido1 = self.lance_plissada(obj,Perfil[0])

			solido2 = self.lance_plissada(obj,Perfil[1])
			solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
			solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

			solido3 = self.degraus_plissada(obj)
			solido3.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

			solido4 = Part.Compound([solido1,solido2,solido3])
			obj.Shape = solido4

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Sim' and obj.TipoDegrau == 'Plissada':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_plissada(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_plissada(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido3 = self.lance_plissada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido4 = self.patamar_plissada(obj, comprimento = obj.Largura)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.patamar_plissada(obj, comprimento = (obj.Largura + (obj.DistLances-(n_degraus_lances[1]*obj.Piso))),recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances-(obj.DistLances-(n_degraus_lances[1]*obj.Piso)),n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido2,solido3,solido4,solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_plissada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido4 = self.patamar_plissada(obj, comprimento = (2*obj.Largura) + obj.DistLances,rotacionar = True)
				solido4.translate(FreeCAD.Vector(obj.DistLances+obj.Largura,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = Part.Compound([solido1,solido3, solido4])
				obj.Shape = solido5

		elif obj.TipoEscada == 'Escada U' and obj.Patamar == 'Não' and obj.TipoDegrau == 'Plissada':###################################
			#gerando os espelhos patamar 1
			solido1 = self.lance_plissada(obj,Perfil[0])

			if n_degraus_lances[1] > 0: # se existir o lance intermediario
				solido2 = self.lance_plissada(obj,Perfil[1])
				solido2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+3)*obj.Espelho))

				solido3 = self.lance_plissada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+6)*obj.Espelho))

				solido4 = self.degraus_plissada(obj)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_plissada(obj,recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+n_degraus_lances[1]+4)*obj.Espelho))


				solido6 = Part.Compound([solido1,solido2,solido3, solido4, solido5])
				obj.Shape = solido6

			else:
				solido3 = self.lance_plissada(obj,Perfil[2])
				solido3.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+6)*obj.Espelho))

				solido4 = self.degraus_plissada(obj)
				solido4.translate(FreeCAD.Vector(0,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+1)*obj.Espelho))

				solido5 = self.degraus_plissada(obj,recuo = True)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.DistLances,n_degraus_lances[0]*obj.Piso,(n_degraus_lances[0]+4)*obj.Espelho))

				solido6 = Part.Compound([solido1,solido3,solido4,solido5])
				obj.Shape = solido6


	#Cria os lances das escadas com o perfil comun fechada
	def lance_comum_fechada(self,obj,lance,altura):
		arestas = []
		for i in range(1,len(lance) + 1):
			p1 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i-1)*obj.Espelho)
			p2 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i)*obj.Espelho)
			l = Part.LineSegment(p1,p2).toShape()
			arestas.append(l)
			arestas.append(lance[i-1])

		if altura == 0:
			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(0, len(lance)*obj.Piso,0)
			p3 = FreeCAD.Vector(0, len(lance)*obj.Piso, len(lance)*obj.Espelho)
			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			arestas.append(l1)
			arestas.append(l2)

		else:
			pass
			p0 = FreeCAD.Vector(0,0,0)
			p1 = FreeCAD.Vector(0,0,-altura)
			p2 = FreeCAD.Vector(0, len(lance)*obj.Piso,-altura)
			p3 = FreeCAD.Vector(0,len(lance)*obj.Piso,(len(lance)*obj.Espelho))
			l0 = Part.LineSegment(p0,p1).toShape()
			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			arestas.append(l0)
			arestas.append(l1)
			arestas.append(l2)

		linha = Part.Wire(arestas)
		face = Part.Face(linha)
		solido = face.extrude(FreeCAD.Vector(-obj.Largura,0,0))
		return solido

	def lance_comum_aberta(self,obj,lance):
		arestas = []
		for i in range(1,len(lance) + 1):
			p1 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i-1)*obj.Espelho)
			p2 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i)*obj.Espelho)
			l = Part.LineSegment(p1,p2).toShape()
			arestas.append(l)
			arestas.append(lance[i-1])

		h = len(lance)*obj.Espelho # altura do lance
		l = len(lance)*obj.Piso # comprimento do lance
		d = obj.EspecuraEstrutura
		x = d/math.atan(h/l) #distancia x da base
		y = (h*(l-x))/l

		p0 = FreeCAD.Vector(0,0,0)
		p1 = FreeCAD.Vector(0,x,0)
		p2 = FreeCAD.Vector(0,l,y)
		p3 = FreeCAD.Vector(0,l,h)

		l0 = Part.LineSegment(p0,p1).toShape()
		l1 = Part.LineSegment(p1,p2).toShape()
		l2 = Part.LineSegment(p2,p3).toShape()
		arestas.append(l0)
		arestas.append(l1)
		arestas.append(l2)


		linha = Part.Wire(arestas)
		face = Part.Face(linha)
		solido = face.extrude(FreeCAD.Vector(-obj.Largura,0,0))
		return solido

	def lance_vazada(self,obj,lance):
		degraus = []
		for i in lance:
			linha = Part.Wire(i)
			face = linha.extrude(FreeCAD.Vector(-obj.Largura,0,0))
			solido = face.extrude(FreeCAD.Vector(0,0,-obj.EspecuraDegrau))
			degraus.append(solido)

		solido = Part.Compound(degraus)
		return solido

	def lance_plissada(self,obj,lance):
		arestas = []
		for i in range(1,len(lance) + 1):
			p1 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i-1)*obj.Espelho)
			p2 = FreeCAD.Vector(0,(i-1)*obj.Piso,(i)*obj.Espelho)
			l = Part.LineSegment(p1,p2).toShape()
			arestas.append(l)
			arestas.append(lance[i-1])

		linha = Part.Wire(arestas)
		face = linha.extrude(FreeCAD.Vector(-obj.Largura,0,0))
		solido = face.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

		return solido



	def patamar_fechada(self,obj, altura = 0,comprimento = 0):

		print('ok')
		if obj.TipoEscada == 'Escada reta':
			face = Part.makePlane(obj.Largura,obj.LarguraPatamar,FreeCAD.Vector(0,0,1))
			solido = face.extrude(FreeCAD.Vector(0,0,-altura))

		elif obj.TipoEscada == 'Escada L':
			face = Part.makePlane(obj.Largura,obj.Largura,FreeCAD.Vector(0,0,1))
			solido = face.extrude(FreeCAD.Vector(0,0,-altura))

		elif obj.TipoEscada == 'Escada U':
			if obj.DistLances < obj.Piso:
				face = Part.makePlane((obj.Largura*2)+obj.DistLances,obj.Largura,FreeCAD.Vector(0,0,1))
				solido = face.extrude(FreeCAD.Vector(0,0,-altura))
			else:
				print(comprimento)
				face = Part.makePlane(comprimento,obj.Largura,FreeCAD.Vector(0,0,1))
				solido = face.extrude(FreeCAD.Vector(0,0,-altura))

		return solido

	def patamar_aberta(self,obj,lance,comprimento = 0,recuo = False):

		h = len(lance)*obj.Espelho # altura do lance
		l = len(lance)*obj.Piso # comprimento do lance
		d = obj.EspecuraEstrutura
		x = d/math.atan(h/l) #distancia x da base
		y = (h*x)/l
		ang = math.atan(h/l)
		y2 = x * math.tan(ang)

		if obj.TipoEscada == 'Escada reta':

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(0,0,-(y+obj.Espelho))
			p3 = FreeCAD.Vector(0,x,-y2)
			p4 = FreeCAD.Vector(0,obj.LarguraPatamar,-y2)
			p5 = FreeCAD.Vector(0,obj.LarguraPatamar+obj.Piso,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p4).toShape()
			l4 = Part.LineSegment(p4,p5).toShape()
			l5 = Part.LineSegment(p5,p1).toShape()

			linha = Part.Wire([l1,l2,l3,l4,l5])
			face = Part.Face(linha)
			solido = face.extrude(FreeCAD.Vector(-obj.Largura,0,0))
			return solido

		elif obj.TipoEscada == 'Escada L' or obj.TipoEscada == 'Escada U':
			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(0,0,-(y+obj.Espelho))
			p3 = FreeCAD.Vector(0,x,-y2)

			if recuo == False:
				p4 = FreeCAD.Vector(0,obj.Largura,-y2)
				p5 = FreeCAD.Vector(0,obj.Largura,0)

			else:
				p4 = FreeCAD.Vector(0,obj.Largura+(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),-y2)
				p5 = FreeCAD.Vector(0,obj.Largura+(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0)


			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p4).toShape()
			l4 = Part.LineSegment(p4,p5).toShape()
			l5 = Part.LineSegment(p5,p1).toShape()

			linha = Part.Wire([l1,l2,l3,l4,l5])
			face = Part.Face(linha)
			solido = face.extrude(FreeCAD.Vector(-comprimento,0,0))


			p6 = FreeCAD.Vector(0,0,0)
			p7 = FreeCAD.Vector(0,0,-obj.Espelho)
			p8 = FreeCAD.Vector(obj.Piso,0,0)

			l6 = Part.LineSegment(p6,p7).toShape()
			l7 = Part.LineSegment(p7,p8).toShape()
			l8 = Part.LineSegment(p8,p6).toShape()

			if recuo == False:
				linha2 = Part.Wire([l6,l7,l8])
				face2 = Part.Face(linha2)
				solido2 = face2.extrude(FreeCAD.Vector(0,obj.Largura,0))
			else:
				linha2 = Part.Wire([l6,l7,l8])
				face2 = Part.Face(linha2)

				face2.translate(FreeCAD.Vector(0,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),0))
				solido2 = face2.extrude(FreeCAD.Vector(0,obj.Largura,0))

			if obj.DistLances < obj.Piso and obj.TipoEscada == 'Escada U':
				solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(-(obj.DistLances+obj.Largura),0,0))

			
			solido3 = Part.Compound([solido,solido2])
			return solido3
			
	def patamar_vazada(self,obj,comprimento = 0):
		if obj.TipoEscada == 'Escada reta':

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			linha = Part.Wire([l1])
			face = linha.extrude(FreeCAD.Vector(0,obj.LarguraPatamar,0))
			solido1 = face.extrude(FreeCAD.Vector(0,0, -obj.EspecuraDegrau))
			solido1.translate(FreeCAD.Vector(0,0,0))

			return solido1

		elif obj.TipoEscada == 'Escada L':

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			linha = Part.Wire([l1])
			face = linha.extrude(FreeCAD.Vector(0,obj.Largura,0))
			solido1 = face.extrude(FreeCAD.Vector(0,0, -obj.EspecuraDegrau))
			solido1.translate(FreeCAD.Vector(0,0,5))

			return solido1

		elif obj.TipoEscada == 'Escada U':

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-comprimento,0,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			linha = Part.Wire([l1])
			face = linha.extrude(FreeCAD.Vector(0,obj.Largura,0))
			solido1 = face.extrude(FreeCAD.Vector(0,0, -obj.EspecuraDegrau))
			solido1.translate(FreeCAD.Vector(0,0,5))

			return solido1

	def patamar_plissada(self,obj,comprimento = 0,recuo = False, rotacionar = False):
		if obj.TipoEscada == 'Escada reta':

			p1 = FreeCAD.Vector(0,0,-obj.Espelho)
			p2 = FreeCAD.Vector(0,0,0)
			p3 = FreeCAD.Vector(0,obj.LarguraPatamar,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()

			linha = Part.Wire([l1,l2])
			face = linha.extrude(FreeCAD.Vector(-obj.Largura,0,0))
			solido = face.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			return solido

		elif obj.TipoEscada == 'Escada L':

			#espelho
			p1 = FreeCAD.Vector(0,0,-obj.Espelho)
			p2 = FreeCAD.Vector(0,0,0)
			l1 = Part.LineSegment(p1,p2).toShape()
			linha = Part.Wire([l1])
			face = linha.extrude(FreeCAD.Vector(-obj.Largura,0,0))
			solido1 = face.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			#patamar
			p3 = FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau)
			p4 = FreeCAD.Vector(0,obj.Largura,-obj.EspecuraDegrau)
			p5 = FreeCAD.Vector(0,obj.Largura,0)

			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p4).toShape()
			l4 = Part.LineSegment(p4,p5).toShape()
			l5 = Part.LineSegment(p5,p2).toShape()
			linha2 = Part.Wire([l2,l3,l4,l5])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(-obj.Largura,0,0))

			#complemento triangular
			p6 = FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau)
			p7 = FreeCAD.Vector(0,0,-obj.EspecuraDegrau)


			l6 = Part.LineSegment(p2,p6).toShape()
			l7 = Part.LineSegment(p6,p7).toShape()
			l8 = Part.LineSegment(p7,p2).toShape()
			linha3 = Part.Wire([l6,l7,l8])
			face3= Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(0,obj.Largura,0))

			solido4 = Part.Compound([solido1,solido2,solido3])

			return solido4

		elif obj.TipoEscada == 'Escada U':

			#espelho
			p1 = FreeCAD.Vector(0,0,-obj.Espelho)
			p2 = FreeCAD.Vector(0,0,0)
			l1 = Part.LineSegment(p1,p2).toShape()
			linha = Part.Wire([l1])
			face = linha.extrude(FreeCAD.Vector(-obj.Largura,0,0))

			if rotacionar == False:
				solido1 = face.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))
			else:
				solido1 = face.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))
				solido1.translate(FreeCAD.Vector(-obj.Largura-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0,0))

			#patamar
			p3 = FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau)
			if rotacionar == False:
				p4 = FreeCAD.Vector(0,comprimento,-obj.EspecuraDegrau)
				p5 = FreeCAD.Vector(0,comprimento,0)
			else:
				p4 = FreeCAD.Vector(0,obj.Largura,-obj.EspecuraDegrau)
				p5 = FreeCAD.Vector(0,obj.Largura,0)


			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p4).toShape()
			l4 = Part.LineSegment(p4,p5).toShape()
			l5 = Part.LineSegment(p5,p2).toShape()
			linha2 = Part.Wire([l2,l3,l4,l5])
			face2 = Part.Face(linha2)

			if rotacionar == False:
				solido2 = face2.extrude(FreeCAD.Vector(-obj.Largura,0,0))	
			else:
				solido2 = face2.extrude(FreeCAD.Vector(-comprimento,0,0))


				


			#complemento triangular 1
			p6 = FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau)
			p7 = FreeCAD.Vector(0,0,-obj.EspecuraDegrau)

			if recuo == False:
				p6 = FreeCAD.Vector(0,0,0)
				p7 = FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau)
				p8 = FreeCAD.Vector(0,0,-obj.EspecuraDegrau)
			else:
				p6 = FreeCAD.Vector(0,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),0)
				p7 = FreeCAD.Vector(obj.EspecuraDegrau,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),-obj.EspecuraDegrau)
				p8 = FreeCAD.Vector(0,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),-obj.EspecuraDegrau)

			l6 = Part.LineSegment(p6,p7).toShape()
			l7 = Part.LineSegment(p7,p8).toShape()
			l8 = Part.LineSegment(p8,p6).toShape()
			linha3 = Part.Wire([l6,l7,l8])
			face3= Part.Face(linha3)

			if recuo == False:#
				if rotacionar == False:
					solido3 = face3.extrude(FreeCAD.Vector(0,obj.

						Largura,0))
				else:
					solido3 = face3.extrude(FreeCAD.Vector(0,obj.Largura,0))
					solido3.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
					solido3.translate(FreeCAD.Vector(-obj.Largura,0,0))
			else:
				solido3 = face3.extrude(FreeCAD.Vector(0,obj.Largura,0))


			#complemento triangular 2
			if rotacionar == True: # patamar inteiro
				p6 = FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau)
				p7 = FreeCAD.Vector(0,0,-obj.EspecuraDegrau)

				if recuo == False:
					p6 = FreeCAD.Vector(0,0,0)
					p7 = FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau)
					p8 = FreeCAD.Vector(0,0,-obj.EspecuraDegrau)
				else:
					p6 = FreeCAD.Vector(0,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),0)
					p7 = FreeCAD.Vector(obj.EspecuraDegrau,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),-obj.EspecuraDegrau)
					p8 = FreeCAD.Vector(0,obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso),-obj.EspecuraDegrau)

				l6 = Part.LineSegment(p6,p7).toShape()
				l7 = Part.LineSegment(p7,p8).toShape()
				l8 = Part.LineSegment(p8,p6).toShape()
				linha3 = Part.Wire([l6,l7,l8])
				face3= Part.Face(linha3)

				if recuo == False:				
					solido4 = face3.extrude(FreeCAD.Vector(0,obj.Largura,0))
					solido4.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-270)
					solido4.translate(FreeCAD.Vector(0,0,0))
				else:
					solido4 = face3.extrude(FreeCAD.Vector(0,comprimento,0))

			if rotacionar == False:
				solido4 = Part.Compound([solido1,solido2,solido3])
				return solido4
			else:
				solido5 = Part.Compound([solido1,solido2,solido3,solido4])
				return solido5



	def degraus_fechada(self,obj,altura,recuo = False):

		if obj.TipoEscada == 'Escada L' or obj.TipoEscada == 'Escada U':

			if recuo == False:
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(-obj.Largura,0,0)
				p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
				p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
				p5 = FreeCAD.Vector(-obj.Largura/2,obj.Largura,0)
				p6 = FreeCAD.Vector(0,obj.Largura,0)

				l1 = Part.LineSegment(p1,p2).toShape()
				l2 = Part.LineSegment(p2,p3).toShape()
				l3 = Part.LineSegment(p3,p1).toShape()

				l4 = Part.LineSegment(p1,p3).toShape()
				l5 = Part.LineSegment(p3,p4).toShape()
				l6 = Part.LineSegment(p4,p5).toShape()
				l7 = Part.LineSegment(p5,p1).toShape()

				l8 = Part.LineSegment(p1,p5).toShape()
				l9 = Part.LineSegment(p5,p6).toShape()
				l10 = Part.LineSegment(p6,p1).toShape()


				linha1 = Part.Wire([l1,l2,l3])
				face1 = Part.Face(linha1)
				solido1 = face1.extrude(FreeCAD.Vector(0,0,-altura))


				linha2 = Part.Wire([l4,l5,l6,l7])
				face2 = Part.Face(linha2)
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-altura-obj.Espelho))
				solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))


				linha3 = Part.Wire([l8,l9,l10])
				face3 = Part.Face(linha3)
				solido3 = face3.extrude(FreeCAD.Vector(0,0,-altura-(2*obj.Espelho)))
				solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))

				solido4 = Part.Compound([solido1,solido2,solido3])
				return solido4

			else:
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(-obj.Largura,0,0)
				p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
				p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
				p5 = FreeCAD.Vector(-(obj.Largura*2)/3,obj.Largura,0)
				p6 = FreeCAD.Vector(0,obj.Largura,0)

				p7 = FreeCAD.Vector(0,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0)
				p8 = FreeCAD.Vector(-obj.Largura,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)))

				l1 = Part.LineSegment(p1,p7).toShape()
				l2 = Part.LineSegment(p7,p8).toShape()
				l3 = Part.LineSegment(p8,p3).toShape()
				l11 = Part.LineSegment(p3,p1).toShape()

				l4 = Part.LineSegment(p1,p3).toShape()
				l5 = Part.LineSegment(p3,p4).toShape()
				l6 = Part.LineSegment(p4,p5).toShape()
				l7 = Part.LineSegment(p5,p1).toShape()

				l8 = Part.LineSegment(p1,p5).toShape()
				l9 = Part.LineSegment(p5,p6).toShape()
				l10 = Part.LineSegment(p6,p1).toShape()

				#DEGRAU1
				linha1 = Part.Wire([l1,l2,l3,l11])
				face1 = Part.Face(linha1)
				solido1 = face1.extrude(FreeCAD.Vector(0,0,-altura))

				#DEGRAU2
				linha2 = Part.Wire([l4,l5,l6,l7])
				face2 = Part.Face(linha2)
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-altura-obj.Espelho))
				solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))

				#DEGRAU3
				linha3 = Part.Wire([l8,l9,l10])
				face3 = Part.Face(linha3)
				solido3 = face3.extrude(FreeCAD.Vector(0,0,-altura-(2*obj.Espelho)))
				solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))

				solido4 = Part.Compound([solido1,solido2,solido3])
				return solido4

	def degraus_aberta(self,obj,recuo = False, triangulo = True):

		if recuo == False:
		
			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-obj.Largura/2,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()


			linha1 = Part.Wire([l1,l2,l3])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,0,-obj.Espelho*2))


			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(0,0,-(2*obj.Espelho)))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))


			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(0,0,-(2*obj.Espelho)))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			if triangulo == True:
				#triangulo de fechamento
				p7 = FreeCAD.Vector(0,0,0)
				p8 = FreeCAD.Vector(0,0,-obj.Espelho)
				p9 = FreeCAD.Vector(obj.Piso,0,0)

				l11 = Part.LineSegment(p7,p8).toShape()
				l12 = Part.LineSegment(p8,p9).toShape()
				l13 = Part.LineSegment(p9,p7).toShape()

			
				linha4 = Part.Wire([l11,l12,l13])
				face4 = Part.Face(linha4)
				solido4 = face4.extrude(FreeCAD.Vector(0,obj.Largura,0))
				solido4.translate(FreeCAD.Vector(0,0,2*obj.Espelho))
				
				solido5 = Part.Compound([solido1,solido2,solido3,solido4])
				return solido5

			else:
				solido5 = Part.Compound([solido1,solido2,solido3])
				return solido5


		else:

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-(obj.Largura*2)/3,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			p7 = FreeCAD.Vector(0,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0)
			p8 = FreeCAD.Vector(-obj.Largura,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)))

			l1 = Part.LineSegment(p1,p7).toShape()
			l2 = Part.LineSegment(p7,p8).toShape()
			l3 = Part.LineSegment(p8,p3).toShape()
			l11 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()

			#DEGRAU1
			linha1 = Part.Wire([l1,l2,l3,l11])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,0,-obj.Espelho*2))

			#DEGRAU2
			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(0,0,-obj.Espelho*2))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#DEGRAU3
			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(0,0,-obj.Espelho*2))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			#triangulo de fechamento
			p9 = FreeCAD.Vector(0,0,0)
			p10 = FreeCAD.Vector(0,0,-obj.Espelho)
			p11 = FreeCAD.Vector(obj.Piso,0,0)

			l12 = Part.LineSegment(p9,p10).toShape()
			l13 = Part.LineSegment(p10,p11).toShape()
			l14 = Part.LineSegment(p11,p9).toShape()

			linha4 = Part.Wire([l12,l13,l14])
			face4 = Part.Face(linha4)
			face4.translate(FreeCAD.Vector(0,0,obj.Espelho*2))
			solido4 = face4.extrude(FreeCAD.Vector(0,obj.Largura,0))

			solido5 = Part.Compound([solido1,solido2,solido3,solido4])
			return solido5

	def degraus_vazada(self,obj,recuo = False):
		if recuo == False:
		
			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-obj.Largura/2,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()


			linha1 = Part.Wire([l1,l2,l3])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,0,-obj.EspecuraDegrau))


			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(0,0,-(obj.EspecuraDegrau)))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))


			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(0,0,-(obj.EspecuraDegrau)))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))

			solido5 = Part.Compound([solido1,solido2,solido3])
			return solido5

		else:

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-(obj.Largura*2)/3,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			p7 = FreeCAD.Vector(0,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0)
			p8 = FreeCAD.Vector(-obj.Largura,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)))

			l1 = Part.LineSegment(p1,p7).toShape()
			l2 = Part.LineSegment(p7,p8).toShape()
			l3 = Part.LineSegment(p8,p3).toShape()
			l11 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()

			#DEGRAU1
			linha1 = Part.Wire([l1,l2,l3,l11])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,0,-obj.EspecuraDegrau))

			#DEGRAU2
			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(0,0,-obj.EspecuraDegrau))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#DEGRAU3
			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(0,0,-obj.EspecuraDegrau))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			solido5 = Part.Compound([solido1,solido2,solido3])
			return solido5

	def degraus_plissada(self,obj,recuo = False):
		if recuo == False:
		
			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-obj.Largura/2,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			l1 = Part.LineSegment(p1,p2).toShape()
			l2 = Part.LineSegment(p2,p3).toShape()
			l3 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()

			#degraus 1
			linha1 = Part.Wire([l1,l2,l3])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			#degraus 2
			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-(obj.EspecuraDegrau)))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#degraus 3
			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-(obj.EspecuraDegrau)))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			#espelho 1
			linha4 = Part.Wire([l1])
			face4 = linha4.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido4 = face4.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			#espelho 2
			linha5 = Part.Wire([l4])
			face5 = linha5.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido5 = face5.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))
			solido5.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#espelho 3
			linha6 = Part.Wire([l8])
			face6 = linha6.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido6 = face6.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau))
			solido6.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			solido7 = Part.Compound([solido1,solido2,solido3,solido4,solido5,solido6])
			return solido7

		else:

			p1 = FreeCAD.Vector(0,0,0)
			p2 = FreeCAD.Vector(-obj.Largura,0,0)
			p3 = FreeCAD.Vector(-obj.Largura,obj.Largura/2,0)
			p4 = FreeCAD.Vector(-obj.Largura,obj.Largura,0)
			p5 = FreeCAD.Vector(-(obj.Largura*2)/3,obj.Largura,0)
			p6 = FreeCAD.Vector(0,obj.Largura,0)

			p7 = FreeCAD.Vector(0,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)),0)
			p8 = FreeCAD.Vector(-obj.Largura,-(obj.DistLances-(math.floor(obj.DistLances/obj.Piso)*obj.Piso)))

			l1 = Part.LineSegment(p1,p7).toShape()
			l2 = Part.LineSegment(p7,p8).toShape()
			l3 = Part.LineSegment(p8,p3).toShape()
			l11 = Part.LineSegment(p3,p1).toShape()

			l4 = Part.LineSegment(p1,p3).toShape()
			l5 = Part.LineSegment(p3,p4).toShape()
			l6 = Part.LineSegment(p4,p5).toShape()
			l7 = Part.LineSegment(p5,p1).toShape()

			l8 = Part.LineSegment(p1,p5).toShape()
			l9 = Part.LineSegment(p5,p6).toShape()
			l10 = Part.LineSegment(p6,p1).toShape()

			#degraus 1
			linha1 = Part.Wire([l1,l2,l3,l11])
			face1 = Part.Face(linha1)
			solido1 = face1.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			#degraus 2
			linha2 = Part.Wire([l4,l5,l6,l7])
			face2 = Part.Face(linha2)
			solido2 = face2.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-(obj.EspecuraDegrau)))
			solido2.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#degraus 3
			linha3 = Part.Wire([l8,l9,l10])
			face3 = Part.Face(linha3)
			solido3 = face3.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-(obj.EspecuraDegrau)))
			solido3.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			#espelho 1
			linha4 = Part.Wire([l2])
			face4 = linha4.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido4 = face4.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))

			#espelho 2
			linha5 = Part.Wire([l4])
			face5 = linha5.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido5 = face5.extrude(FreeCAD.Vector(0,obj.EspecuraDegrau,-obj.EspecuraDegrau))
			solido5.translate(FreeCAD.Vector(0,0,obj.Espelho))

			#espelho 3
			linha6 = Part.Wire([l8])
			face6 = linha6.extrude(FreeCAD.Vector(0,0,-obj.Espelho))
			solido6 = face6.extrude(FreeCAD.Vector(obj.EspecuraDegrau,0,-obj.EspecuraDegrau))
			solido6.translate(FreeCAD.Vector(0,0,2*obj.Espelho))


			solido7 = Part.Compound([solido1,solido2,solido3,solido4,solido5, solido6])
			return solido7



class Longarina:
	def __init__(self, obj,tipoescada,patamar,tipodegrau,tipolongarina,especuraestrutura,
		larguralongarina,altura,largura,ndegraus,especuradegrau,espelho,piso,distlances,mastro,diametroespiral,largurapatamar,base):

		obj.Proxy = self

		obj.addProperty("App::PropertyLink", "Base","Host","Posição da longarina")
		obj.Base = base

		#Estrutura
		obj.addProperty("App::PropertyEnumeration", "TipoLongarina","Estrutura","Posição da longarina")
		obj.TipoLongarina = ['Nenhum','Central','Borda', 'Lateral']
		obj.TipoLongarina = tipolongarina

		obj.addProperty("App::PropertyLength", "LarguraLongarina","Estrutura","Largura da longarina")
		obj.LarguraLongarina = larguralongarina * 10

		obj.addProperty("App::PropertyLength", "EspecuraEstrutura","Estrutura","Espeçura da estrutura e longarinas")
		obj.EspecuraEstrutura = especuraestrutura * 10

		obj.addProperty("App::PropertyEnumeration", "Mastro","Estrutura","Se sim, adiciona um mastro á escada espiral")
		obj.Mastro = ['Não','Sim']
		obj.Mastro = mastro

		obj.addProperty("App::PropertyLength", "LarguraInicial","Estrutura","Se sim, adiciona um mastro á escada espiral")
		obj.setEditorMode("LarguraInicial", 2)
		obj.LarguraInicial = 920


		#propriedades ocultas
		obj.addProperty("App::PropertyLength", "Recuo","Estrutura")
		obj.setEditorMode('Recuo',2)
		obj.Recuo = 300

	def execute(self,obj):

		n_degraus_lances = []
		# calcula o numero de degraus de cada lance da escada
		if obj.Base.TipoEscada == 'Escada reta' and obj.Base.Patamar == 'Não':
			n_degraus_lances.append(obj.Base.NDegraus)

		elif obj.Base.TipoEscada == 'Escada reta' and obj.Base.Patamar == 'Sim':
			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-1)/2))
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-1)/2))

		elif obj.Base.TipoEscada == 'Escada L' and  obj.Base.Patamar == 'Sim':
			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-1)/2))
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-1)/2))

		elif obj.Base.TipoEscada == 'Escada L' and  obj.Base.Patamar == 'Não':
			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-3)/2))
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-3)/2))

		elif obj.Base.TipoEscada == 'Escada U' and  obj.Base.Patamar == 'Sim' and obj.Base.DistLances < obj.Base.Piso:
			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-1)/2))
			n_degraus_lances.append(0)
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-1)/2))

		elif obj.Base.TipoEscada == 'Escada U' and  obj.Base.Patamar == 'Não' and obj.Base.DistLances < obj.Base.Piso:
			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-6)/2))
			n_degraus_lances.append(0)
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-6)/2))

		elif obj.Base.TipoEscada == 'Escada U' and  obj.Base.Patamar == 'Sim' and obj.Base.DistLances >= obj.Base.Piso:
			degraus_intermediario = math.floor(obj.Base.DistLances/obj.Base.Piso) # calculo do numero de degraus do lance intermediário

			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-degraus_intermediario-2)/2))
			n_degraus_lances.append(degraus_intermediario)
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-degraus_intermediario-2)/2))

		elif obj.Base.TipoEscada == 'Escada U' and  obj.Base.Patamar == 'Não' and obj.Base.DistLances >= obj.Base.Piso:
			degraus_intermediario = math.floor(obj.Base.DistLances/obj.Base.Piso) # calculo do numero de degraus do lance intermediário

			n_degraus_lances.append(math.ceil((obj.Base.NDegraus-degraus_intermediario-6)/2))
			n_degraus_lances.append(degraus_intermediario)
			n_degraus_lances.append(math.floor((obj.Base.NDegraus-degraus_intermediario-6)/2))

		elif obj.Base.TipoEscada == 'Escada espiral':
			n_degraus_lances.append(obj.Base.NDegraus)





		if obj.TipoLongarina == 'Central':

			if obj.Base.TipoEscada == 'Escada reta' and obj.Base.Patamar == 'Não':

				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.Base.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base

				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,(obj.Base.NDegraus)*obj.Base.Piso, obj.Base.NDegraus*obj.Base.Espelho)

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido = face.extrude(FreeCAD.Vector(0,x,0))
				solido.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))

				obj.Shape = solido
				obj.Placement = solido.Placement

			elif obj.Base.TipoEscada == 'Escada reta' and obj.Base.Patamar == 'Sim':
				
				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base
				y = (x*h)/l

				#usado para calcular ospontos do triangulo
				y2 = obj.Base.Espelho - obj.Base.EspecuraDegrau 	
				x2 = (l*y2*1.5)/h

				 #Lance 1
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,(n_degraus_lances[0]*obj.Base.Piso), (n_degraus_lances[0]*obj.Base.Espelho))

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido1 = face.extrude(FreeCAD.Vector(0,0,-y))
				solido1.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				#lance2
				p3 = FreeCAD.Vector(0,0,0)
				p4 = FreeCAD.Vector(0,((n_degraus_lances[1])*obj.Base.Piso), ((n_degraus_lances[1])*obj.Base.Espelho))

				l2 = Part.LineSegment(p3,p4).toShape()
				linha2 = Part.Wire([l2])
				face2 = linha2.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-y))
				solido2.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,((n_degraus_lances[0])*obj.Base.Piso)+obj.Base.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Base.Espelho))  


				#patamar
				p5 = FreeCAD.Vector(0,(n_degraus_lances[0])*obj.Base.Piso,(n_degraus_lances[0]+1)*obj.Base.Espelho)
				p6 = FreeCAD.Vector(0,((n_degraus_lances[0])*obj.Base.Piso)+obj.Base.LarguraPatamar,(n_degraus_lances[0]+1)*obj.Base.Espelho)

				l3 = Part.LineSegment(p5,p6).toShape()
				linha3 = Part.Wire([l3])
				face3 = linha3.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido3 = face3.extrude(FreeCAD.Vector(0,0,-(y-obj.Base.EspecuraDegrau)))
				solido3.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,-obj.Base.EspecuraDegrau))

				#triangulo
				p7 = FreeCAD.Vector(0,(n_degraus_lances[0])*obj.Base.Piso,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y)
				p8 = FreeCAD.Vector(0,(n_degraus_lances[0])*obj.Base.Piso,((n_degraus_lances[0])*obj.Base.Espelho)-y)
				p9 = FreeCAD.Vector(0,(n_degraus_lances[0]*obj.Base.Piso)+x2, ((n_degraus_lances[0]+1)*obj.Base.Espelho)-y)

				l4 = Part.LineSegment(p7,p8).toShape()
				l5 = Part.LineSegment(p8,p9).toShape()
				l6 = Part.LineSegment(p9,p7).toShape()

				linha4 = Part.Wire([l4,l5,l6])
				face4 = Part.Face(linha4)
				solido4 = face4.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido4.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				solido5 = Part.Compound([solido1,solido2,solido3,solido4])	
				obj.Shape = solido5
				obj.Placement = solido5.Placement



			elif obj.Base.TipoEscada == 'Escada L' and obj.Base.Patamar == 'Não':
				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base
				y = (x*h)/l

				#Lance 1
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,((n_degraus_lances[0]+1.5)*obj.Base.Piso), ((n_degraus_lances[0]+1.5)*obj.Base.Espelho))

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido1 = face.extrude(FreeCAD.Vector(0,0,-y))
				solido1.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				#lance2
				p3 = FreeCAD.Vector(0,-obj.Base.Piso*1.5,-obj.Base.Espelho*1.5)
				p4 = FreeCAD.Vector(0,((n_degraus_lances[1])*obj.Base.Piso), ((n_degraus_lances[1])*obj.Base.Espelho))

				l2 = Part.LineSegment(p3,p4).toShape()
				linha2 = Part.Wire([l2])
				face2 = linha2.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-y))
				solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,((n_degraus_lances[0])*obj.Base.Piso)+((obj.Base.Largura+obj.LarguraLongarina)/2),(n_degraus_lances[0]+3)*obj.Base.Espelho))  

				#viga dopatamar 1
				solido3 = Part.makeBox((obj.LarguraLongarina/2)+(obj.Base.Largura-obj.LarguraInicial)/2,obj.LarguraLongarina,y)
				solido3.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+2)*obj.Base.Espelho)-obj.Base.EspecuraDegrau-y-(obj.LarguraInicial*0.0155)))

				try:
					#viga dopatamar 2
					solido4 = Part.makeBox(((obj.LarguraLongarina/2)+(obj.Base.Largura-obj.LarguraInicial)/2)-obj.LarguraLongarina,obj.LarguraLongarina,y)
					solido4.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
					solido4.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+2)*obj.Base.Espelho)-obj.Base.EspecuraDegrau-y-(obj.LarguraInicial*0.0155)))

					solido5 = Part.Compound([solido1,solido2,solido3,solido4])	
					obj.Shape = solido5
					obj.Placement = solido5.Placement
				except:

					solido5 = Part.Compound([solido1,solido2,solido3])	
					obj.Shape = solido5
					obj.Placement = solido5.Placement


			elif  obj.Base.TipoEscada == 'Escada L' and obj.Base.Patamar == 'Sim':
				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base
				y = (x*h)/l

				#Lance 1
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,((n_degraus_lances[0]+1)*obj.Base.Piso), ((n_degraus_lances[0]+1)*obj.Base.Espelho))

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido1 = face.extrude(FreeCAD.Vector(0,0,-y))
				solido1.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				#lance2
				p3 = FreeCAD.Vector(0,0,0)
				p4 = FreeCAD.Vector(0,((n_degraus_lances[1])*obj.Base.Piso), ((n_degraus_lances[1])*obj.Base.Espelho))

				l2 = Part.LineSegment(p3,p4).toShape()
				linha2 = Part.Wire([l2])
				face2 = linha2.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-y))
				solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,((n_degraus_lances[0])*obj.Base.Piso)+((obj.Base.Largura+obj.LarguraLongarina)/2),(n_degraus_lances[0]+1)*obj.Base.Espelho))  

				#viga do patamar 1
				solido3 = Part.makeBox((obj.LarguraLongarina + obj.Base.Largura)/2,obj.LarguraLongarina,y)
				solido3.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))

				try:
					#viga dopatamar 2
					solido4 = Part.makeBox(((obj.LarguraLongarina)+(obj.Base.Largura-obj.LarguraInicial)/2),obj.LarguraLongarina,y)
					solido4.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
					solido4.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))

					solido5 = Part.Compound([solido1,solido2,solido3,solido4])	
					obj.Shape = solido5
					obj.Placement = solido5.Placement
				except:

					solido5 = Part.Compound([solido1,solido2,solido3])	
					obj.Shape = solido5
					obj.Placement = solido5.Placement

			elif  obj.Base.TipoEscada == 'Escada U' and obj.Base.Patamar == 'Sim' and n_degraus_lances[1]  == 0:
				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base
				y = (x*h)/l

				#Lance 1
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,((n_degraus_lances[0]+1)*obj.Base.Piso), ((n_degraus_lances[0]+1)*obj.Base.Espelho))

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido1 = face.extrude(FreeCAD.Vector(0,0,-y))
				solido1.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				#lance2
				p3 = FreeCAD.Vector(0,0,0)
				p4 = FreeCAD.Vector(0,((n_degraus_lances[2])*obj.Base.Piso), ((n_degraus_lances[2])*obj.Base.Espelho))

				l2 = Part.LineSegment(p3,p4).toShape()
				linha2 = Part.Wire([l2])
				face2 = linha2.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-y))
				solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-180)
				solido2.translate(FreeCAD.Vector(obj.Base.DistLances+(obj.Base.Largura+obj.LarguraLongarina)/2,((n_degraus_lances[0])*obj.Base.Piso),(n_degraus_lances[0]+1)*obj.Base.Espelho))  

				#viga do patamar 1
				solido3 = Part.makeBox((obj.LarguraLongarina + obj.Base.Largura)+obj.Base.DistLances,obj.LarguraLongarina,y)
				solido3.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))

				
				#viga dopatamar 2
				solido4 = Part.makeBox(((obj.LarguraLongarina)+(obj.Base.Largura-obj.LarguraInicial)/2),obj.LarguraLongarina,y)
				solido4.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido4.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))


				#viga dopatamar 3
				solido5 = Part.makeBox(((obj.Base.Largura-obj.LarguraLongarina)/2),obj.LarguraLongarina,y)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(obj.Base.DistLances+(obj.Base.Largura-obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))



				solido6 = Part.Compound([solido1,solido2,solido3,solido4, solido5])	
				obj.Shape = solido6
				obj.Placement = solido6.Placement

			elif  obj.Base.TipoEscada == 'Escada U' and obj.Base.Patamar == 'Sim' and n_degraus_lances[1]  > 0:
				h = n_degraus_lances[0]*obj.Base.Espelho # altura do lance
				l = n_degraus_lances[0]*obj.Base.Piso # comprimento do lance
				d = obj.EspecuraEstrutura
				x = d/math.atan(h/l) #distancia x da base
				y = (x*h)/l

				#Lance 1
				p1 = FreeCAD.Vector(0,0,0)
				p2 = FreeCAD.Vector(0,((n_degraus_lances[0]+1)*obj.Base.Piso), ((n_degraus_lances[0]+1)*obj.Base.Espelho))

				l1 = Part.LineSegment(p1,p2).toShape()
				linha = Part.Wire([l1])
				face = linha.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido1 = face.extrude(FreeCAD.Vector(0,0,-y))
				solido1.translate(FreeCAD.Vector(-(obj.Base.Largura + obj.LarguraLongarina)/2,0,0))


				#lance2
				p3 = FreeCAD.Vector(0,0,0)
				p4 = FreeCAD.Vector(0,((n_degraus_lances[1]+1)*obj.Base.Piso), ((n_degraus_lances[1]+1)*obj.Base.Espelho))

				l2 = Part.LineSegment(p3,p4).toShape()
				linha2 = Part.Wire([l2])
				face2 = linha2.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido2 = face2.extrude(FreeCAD.Vector(0,0,-y))
				solido2.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido2.translate(FreeCAD.Vector(0,((n_degraus_lances[0])*obj.Base.Piso)+((obj.Base.Largura+obj.LarguraLongarina)/2),(n_degraus_lances[0]+1)*obj.Base.Espelho))


				#lance3
				p5 = FreeCAD.Vector(0,0,0)
				p6 = FreeCAD.Vector(0,((n_degraus_lances[2])*obj.Base.Piso), ((n_degraus_lances[2])*obj.Base.Espelho))

				l3 = Part.LineSegment(p5,p6).toShape()
				linha3 = Part.Wire([l3])
				face3 = linha3.extrude(FreeCAD.Vector(obj.LarguraLongarina,0,0))
				solido3 = face3.extrude(FreeCAD.Vector(0,0,-y))
				solido3.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-180)
				solido3.translate(FreeCAD.Vector(obj.Base.DistLances+(obj.Base.Largura+obj.LarguraLongarina)/2,((n_degraus_lances[0])*obj.Base.Piso),(n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Base.Espelho))  

				#viga do patamar 1 (primtiro patamar horizontal)
				solido4 = Part.makeBox((obj.LarguraLongarina + obj.Base.Largura)/2,obj.LarguraLongarina,y)
				solido4.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))

				
				#viga dopatamar 2 (primeiro patamar vertical)
				solido5 = Part.makeBox(((obj.LarguraLongarina)+(obj.Base.Largura-obj.LarguraInicial)/2),obj.LarguraLongarina,y)
				solido5.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido5.translate(FreeCAD.Vector(-(obj.Base.Largura+obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+1)*obj.Base.Espelho)-y))


				#viga dopatamar 3 (segundo patamar vertical)
				solido6 = Part.makeBox(((obj.Base.Largura-obj.LarguraLongarina)/2),obj.LarguraLongarina,y)
				solido6.rotate(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),-90)
				solido6.translate(FreeCAD.Vector(obj.Base.DistLances+(obj.Base.Largura-obj.LarguraLongarina)/2,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Base.Espelho)-y))

				#viga do patamar 4 (segundo patamar horizontal)
				solido7 = Part.makeBox((obj.Base.Largura/2) - obj.Base.Piso + obj.LarguraLongarina + obj.LarguraInicial * 0.0325 ,obj.LarguraLongarina,y)
				solido7.translate(FreeCAD.Vector((n_degraus_lances[1]+1)*obj.Base.Piso,(n_degraus_lances[0]*obj.Base.Piso)+(obj.Base.Largura-obj.LarguraLongarina)/2,((n_degraus_lances[0]+n_degraus_lances[1]+2)*obj.Base.Espelho)-y))


				solido8 = Part.Compound([solido1,solido2,solido3,solido4,solido5, solido6, solido7])	
				obj.Shape = solido8
				obj.Placement = solido8.Placement
				





		
		

					



		
		



painel = EscadaPainel()
FreeCADGui.Control.showDialog(painel) 