import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
import funcoes
import requests
from PyQt5.QtWidgets import QMessageBox, QShortcut

#from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import *
import time
#from PyQt5.QtCore import QDateTime, Qt, QLocale
from PyQt5.QtCore import *
import os

import locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDoubleValidator

app = QtWidgets.QApplication([])
#dialogo = uic.loadUi("login.ui")
#cliente = uic.loadUi("cliente.ui")
cliente = uic.loadUi(r'C:\PROGS\NOVA PASTA\cliente.ui')
#fornecedor  = uic.loadUi(r'C:\PROGS\NOVA PASTA\fornecedor.ui')

def inclui_cli():
	if cliente.nome_cliente.text() == "":
		QMessageBox.about(cliente,"Cadastro de clientes", "Nome deve ser informado !!!")
		return()

	cliente.status_cliente.setText("INCLUIR")
	b_query="insert into tb_clientes (cpf_cliente,cnpj_cliente,nome_cliente,fantasia_cliente,cep_cliente,municipio_cliente,uf_cliente,logradouro_cliente,numero_cliente,complemento_cliente,email_cliente,telefone_cliente,celular_cliente,quem,quando,nascimento_cliente,limite_cliente) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	prepara_d_query("I")
	resultado=funcoes.exec_query(b_query,d_query)
	cliente.id_cliente.setText(str(funcoes.ultimo_id))

	if resultado!=None:
		QMessageBox.critical(cliente,"ERRO","Erro ao inserir o cliente.")
	else:
		QMessageBox.information(cliente,"OK","Cliente inserido com sucesso.")
	cliente.status_cliente.setText("NAVEGAR")

def altera_cli():
	cliente.status_cliente.setText("ALTERAR")
	b_query="update tb_clientes set cpf_cliente=%s,cnpj_cliente=%s,nome_cliente=%s,fantasia_cliente=%s,cep_cliente=%s,municipio_cliente=%s,uf_cliente=%s,logradouro_cliente=%s,numero_cliente=%s,complemento_cliente=%s,email_cliente=%s,telefone_cliente=%s,celular_cliente=%s,quem=%s,quando=%s,nascimento_cliente=%s,limite_cliente=%s where id_cliente=%s"
	prepara_d_query("A")
	resultado=funcoes.exec_query(b_query,d_query)
	#ti=time.time()
	if resultado!=None:
		QMessageBox.critical(cliente,"ERRO","Erro ao alterar o cliente.")
	else:
		QMessageBox.information(cliente,"OK","Cliente alterado com sucesso.")

	#time.sleep(5)

	#tf=time.time()
	#print(tf-ti)
	#print(time.asctime(time.localtime(time.time())))

	cliente.status_cliente.setText("NAVEGAR")
	pega_cliente("=")
def exclui_cli():
	cliente.status_cliente.setText("EXCLUIR")
	opc=QMessageBox.question(cliente,"Exclusão","Confirme a exclusão deste cliente?",QMessageBox.Yes|QMessageBox.No)
	if opc==QMessageBox.Yes:
		QMessageBox.information(cliente,"OK","Cliente será excluido.")
		b_query="DELETE FROM tb_clientes WHERE id_cliente = %s"
		d_query = (cliente.id_cliente.text())
		resultado=funcoes.exec_query(b_query,d_query)
		pega_cliente("<")
		if resultado!=None:
			QMessageBox.critical(cliente,"ERRO","Erro ao excluir o cliente.")
		else:
			QMessageBox.information(cliente,"OK","Cliente excluido com sucesso.")
		cliente.status_cliente.setText("NAVEGAR")

def imprimir_cli():
	b_query="SELECT CONCAT(id_cliente,'     ',LPAD(cpf_cliente,11,' '),'   ',LPAD(cnpj_cliente,14,' '),'   ',RPAD(nome_cliente,40,' '),'   ',cep_cliente,'   ',logradouro_cliente) AS linha FROM tb_clientes"
	d_query=None
	resultado=funcoes.exec_query(b_query,d_query,False)
	MODULO='CLIENTE'
	TP='LISTA ALFABETICA DE'
	TIT1=TP+" "+MODULO
	TIT2="COMPLETA"
	TIT3="DE TODOS"
	lcabrm=125
	funcoes.cabr(cliente.textEdit,TIT1,TIT2,TIT3,len(resultado),lcabrm)
	linha='    CODIGO   CNPJ/CPF      NOME____________________________________   CEP'
	cliente.textEdit.insertPlainText(linha+'\n')
	cliente.textEdit.insertPlainText(("-" * lcabrm)+'\n')
	for registro in resultado:
		#print("linha:",registro['linha'])
		#cliente.textEdit.insertPlainText(registro['linha']+'\n')
		cliente.textEdit.insertPlainText(registro['linha'])
		cliente.textEdit.insertPlainText('\n')

	funcoes.filePreview(cliente.textEdit)

def buscacep():
	if len(cliente.cep_cliente.text()) != 8 or not cliente.cep_cliente.text().isnumeric():
		QMessageBox.about(cliente,"Cadastro de clientes", "CEP informado deve ter 8 digitos numéricos !!!")
		return()

	request = requests.get('http://viacep.com.br/ws/{}/json/'.format(cliente.cep_cliente.text()))
	address_data = request.json()
	if 'erro' not in address_data:
		cliente.logradouro_cliente.setText(address_data['logradouro'].upper())
		cliente.municipio_cliente.setText(address_data['localidade'].upper())
		cliente.uf_cliente.setText(address_data['uf'].upper())
	else:
		QMessageBox.about(cliente,"Cadastro de clientes", "CEP informado não consta no cadastro dos correios !!!")

def buscacnpj():
	if len(cliente.cnpj_cliente.text()) != 14  or not cliente.cnpj_cliente.text().isnumeric(): 
		QMessageBox.about(cliente,"Cadastro de clientes", "CNPJ informado deve ter 14 digitos numéricos !!!")
		return()

	request = requests.get('http://www.receitaws.com.br/v1/cnpj/{0}'.format(cliente.cnpj_cliente.text()))
	address_data = request.json()
	if address_data['status'].upper() == "OK":
		cliente.nome_cliente.setText(address_data['nome'].upper())
		cliente.fantasia_cliente.setText(address_data['fantasia'].upper())
		cliente.logradouro_cliente.setText(address_data['logradouro'].upper())
		cliente.numero_cliente.setText(address_data['numero'].upper())
		cliente.complemento_cliente.setText(address_data['complemento'].upper())
		cliente.cep_cliente.setText(address_data['cep'].upper())
		cliente.municipio_cliente.setText(address_data['municipio'].upper())
		cliente.uf_cliente.setText(address_data['uf'].upper())
		cliente.email_cliente.setText(address_data['email'].upper())
		cliente.telefone_cliente.setText(address_data['telefone'].upper())
	else:
		QMessageBox.about(cliente,"Cadastro de clientes", "CNPJ informado não consta no cadastro dos correios !!!")

def pega_cliente(tipo):
	ordem=" "
	if tipo=="<":
		ordem=" DESC "
	if tipo=="L":
		b_query="SELECT * FROM tb_clientes WHERE nome_cliente LIKE '%"+cliente.nome_cliente.text()+"%'"
		#QMessageBox.information(cliente,"NAVEGADOR",b_query)
	else:
		b_query="SELECT * FROM tb_clientes WHERE id_cliente "+tipo+cliente.id_cliente.text()+" ORDER BY id_cliente"+ordem+" LIMIT 1"
	
	resultado=funcoes.exec_query(b_query)
	if resultado!=None:
		if resultado['id_cliente'] !="":
			cliente.status_cliente.setText("NAVEGAR")
			cliente.id_cliente.setText(str(resultado['id_cliente']))

			cliente.cpf_cliente.setText(str(resultado['cpf_cliente']))
			cliente.cnpj_cliente.setText(str(resultado['cnpj_cliente']))
			cliente.nome_cliente.setText(str(resultado['nome_cliente']))
			cliente.fantasia_cliente.setText(str(resultado['fantasia_cliente']))

			cliente.cep_cliente.setText(str(resultado['cep_cliente']))
			cliente.municipio_cliente.setText(str(resultado['municipio_cliente']))
			cliente.uf_cliente.setText(str(resultado['uf_cliente']))

			cliente.logradouro_cliente.setText(str(resultado['logradouro_cliente']))
			cliente.numero_cliente.setText(str(resultado['numero_cliente']))
			cliente.complemento_cliente.setText(str(resultado['complemento_cliente']))

			cliente.email_cliente.setText(str(resultado['email_cliente']))
			cliente.telefone_cliente.setText(str(resultado['telefone_cliente']))
			cliente.celular_cliente.setText(str(resultado['celular_cliente']))

			cliente.quem.setText(str(resultado['quem']))
			cliente.quando.setText(resultado['quando'].strftime("%A - %d/%m/%Y às %H:%M:%S") if resultado['quando']!=None else str(resultado['quando']))
			cliente.nascimento_cliente.setDate(resultado['nascimento_cliente'] if resultado['nascimento_cliente']!=None else QDate(1800, 10, 22))

			cliente.limite_cliente.setText(str(resultado['limite_cliente']).replace(".",","))


		else:
			QMessageBox.information(cliente,"NAVEGADOR","Está vazio.")
	else:
		QMessageBox.information(cliente,"NAVEGADOR","Não achou nada.")

def prepara_d_query(tipo):
	#cliente.limite_cliente.setText(cliente.limite_cliente.text() if cliente.limite_cliente.text()!="" else "0.00")
	#cliente.limite_cliente.setText(str(f'{float(cliente.limite_cliente.text().replace(",","."))*1.00:.2f}'))
	#print(f'{float(cliente.limite_cliente.text().replace(",",".")):.2f}')
	#print(cliente.limite_cliente.text())
	if cliente.limite_cliente.text() == "":
		cliente.limite_cliente.setText('0')

	global d_query
	d_query= (
cliente.cpf_cliente.text(),
cliente.cnpj_cliente.text(),
cliente.nome_cliente.text().upper(),
cliente.fantasia_cliente.text().upper(),
cliente.cep_cliente.text(),
cliente.municipio_cliente.text().upper(),
cliente.uf_cliente.text().upper(),
cliente.logradouro_cliente.text().upper(),
cliente.numero_cliente.text(),
cliente.complemento_cliente.text().upper(),
cliente.email_cliente.text().lower(),
cliente.telefone_cliente.text(),
cliente.celular_cliente.text(),
dialogo.c_username.text(),
QDateTime.currentDateTime().toString(Qt.ISODate),
cliente.nascimento_cliente.date().toString(Qt.ISODate),
cliente.limite_cliente.text().replace(",","."))


#float(cliente.limite_cliente.text().replace(",",".")))


	if tipo=="A":
		d_query=d_query+( cliente.id_cliente.text(),)

	return d_query

def localizar_cli():
	pega_cliente("L")

def quem():
	QMessageBox.information(cliente,"CONTROL Q","Vai dizer quem pos a mão.")

def num_digitado():
	num_final=cliente.limite_cliente.text().replace(",",".")
	print(num_final)
	#print(float(num_final))
	#str_value = input("Digite a pretenção salarial (exemplo: R${}): ".format(locale.format("%.2f", suggestion)))
	#str_value = cliente.limite_cliente.text().replace(",",".").format("%.2f")
	#print(f'{float(cliente.limite_cliente.text().replace(",",".")):.2f}')
	#print(str_value)
	#locale.format("%.2f", value, grouping=True, monetary=True)

	#cliente.limite_cliente.setLocale(QtCore.QLocale("pt_BR"))
	#print(cliente.limite_cliente.text())
	#cliente.limite_cliente.setValidator(QDoubleValidator(0.00,999999999.99,2))
	#print(cliente.limite_cliente.text())
	


def limpar_cli():
	cliente.id_cliente.clear()
	cliente.cpf_cliente.clear()
	cliente.cnpj_cliente.clear()
	cliente.nome_cliente.clear()
	cliente.fantasia_cliente.clear()
	cliente.cep_cliente.clear()
	cliente.municipio_cliente.clear()
	cliente.uf_cliente.clear()
	cliente.logradouro_cliente.clear()
	cliente.numero_cliente.clear()
	cliente.complemento_cliente.clear()
	cliente.email_cliente.clear()
	cliente.telefone_cliente.clear()
	cliente.celular_cliente.clear()
	cliente.nascimento_cliente.clear()
	cliente.limite_cliente.clear()
	cliente.quem.clear()
	cliente.quando.clear()

def teclou_ponto():
	QMessageBox.information(cliente,".....","teclu ponto")

def buscacep_api():
	if len(cliente.cep_cliente.text()) != 8:
		QMessageBox.about(cliente,"Cadastro de clientes", "CEP informado deve ter 8 digitos !!!")
		return()

	request = requests.get('https://api.postmon.com.br/v1/cep/{}'.format(cliente.cep_cliente.text()))
	address_data = request.json()

	if 'erro' not in address_data:
		print(address_data)
		cliente.logradouro_cliente.setText(address_data['logradouro'].upper())
		cliente.municipio_cliente.setText(address_data['cidade'].upper())
		cliente.uf_cliente.setText(address_data['estado'].upper())
	else:
		QMessageBox.about(cliente,"Cadastro de clientes", "CEP informado não consta no cadastro dos correios !!!")

#novo pushButton

cliente.pb_novo = QtWidgets.QPushButton(cliente.centralwidget)
cliente.pb_novo.setGeometry(QtCore.QRect(490, 360, 75, 23))
cliente.pb_novo.setText("Novo")
cliente.pb_novo.setObjectName("pb_novo")
cliente.pb_novo.clicked.connect(num_digitado)


shortcut_open=QShortcut(QKeySequence('Ctrl+q'),cliente)
shortcut_open.activated.connect(quem)

cliente.id_cliente.setText("10000000")
pega_cliente("<")


#numeros
#loc=QtCore.QLocale()
#print(loc)
#loc.setNumberOptions(QtCore.QLocale.RejectGroupSeparator)
#loc.setNumberOptions(QtCore.QLocale.OmitGroupSeparator)
#print(loc)
#loc=QtCore.QLocale("pt_BR")
#loc.setNumberOptions(QtCore.QLocale.RejectGroupSeparator)
#loc.setNumberOptions(QtCore.QLocale.OmitGroupSeparator)

cliente.limite_cliente.setLocale(QtCore.QLocale("pt_BR"))
cliente.limite_cliente.setValidator(QtGui.QDoubleValidator( 0, 99999, 2, cliente.limite_cliente))


#externo
#os.startfile('notepad.exe')
#os.startfile('http://viacep.com.br/')
#os.startfile('E:/DIA09052020/QT DESIGNER LINK.txt')


cliente.pb_nono.clicked.connect(lambda:os.startfile('notepad.exe'))

cliente.pb_anterior.clicked.connect(lambda:pega_cliente("<"))
cliente.pb_proximo.clicked.connect(lambda:pega_cliente(">"))
cliente.pb_incluir.clicked.connect(inclui_cli)
cliente.pb_alterar.clicked.connect(altera_cli)
cliente.pb_excluir.clicked.connect(exclui_cli)
cliente.pb_busca_cep.clicked.connect(buscacep)
cliente.pb_busca_cnpj.clicked.connect(buscacnpj)
cliente.pb_localizar.clicked.connect(localizar_cli)
cliente.pb_limpar.clicked.connect(limpar_cli)
cliente.pb_calculadora.clicked.connect(lambda:os.startfile('calc.exe'))
cliente.actionPadrao.triggered.connect(imprimir_cli)
#cliente.pb_cep_api.clicked.connect(buscacep_api)
#cliente.pb_cep_api.clicked.connect(cli_simples.simples)



cliente.show()
app.exec_()