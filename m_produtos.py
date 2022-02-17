import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import funcoes

from PyQt5.QtWidgets import QMessageBox



app = QtWidgets.QApplication([])
produtos  = uic.loadUi("produtos.ui")

def procura_pro():
	b_query="SELECT * FROM produtos WHERE codigo =%s"
	d_query=(produtos.c_codigo.text())
	resultado=funcoes.exec_query(b_query,d_query,True)
	produtos.c_barra.clear()
	produtos.c_descricao.clear()
	produtos.c_resumida.clear()
	
	if resultado==None:
		QMessageBox.about(produtos,"Produto","Não cadastrado !!!")
	else:
		produtos.c_codigo.setText(resultado['codigo'])
		produtos.c_barra.setText(resultado['barra'])
		produtos.c_descricao.setText(resultado['descricao'])
		produtos.c_resumida.setText(resultado['resumida'])

def inclui_pro():
	b_query="INSERT INTO produtos(codigo,barra,descricao,resumida) VALUES (%s,%s,%s,%s)"
	d_query=(produtos.c_codigo.text(),produtos.c_barra.text(),produtos.c_descricao.text(),produtos.c_resumida.text())
	resultado=funcoes.exec_query(b_query,d_query)

def altera_pro():
	produtos.c_descricao.setText(produtos.c_descricao.text().upper().lstrip().rstrip())	
	b_query="UPDATE produtos SET barra=%s, descricao=%s, resumida=%s WHERE codigo = %s"
	d_query=(produtos.c_barra.text(),produtos.c_descricao.text(),produtos.c_resumida.text(),produtos.c_codigo.text())
	resultado=funcoes.exec_query(b_query,d_query)

def exclui_pro():
	b_query="DELETE FROM produtos WHERE codigo = %s"
	d_query = (produtos.c_codigo.text())
	resultado=funcoes.exec_query(b_query,d_query)

def imprimir_pro():
	b_query="SELECT (CONCAT(LPAD(codigo,10,' '),'   ',LPAD(barra,14,' '),'   ',RPAD(descricao,40,' '),'   ',LPAD(resumida,20,' '))) AS linha FROM produtos"
	d_query=None
	resultado=funcoes.exec_query(b_query,d_query,False)
	MODULO='PRODUTOS'
	TP='LISTA ALFABETICA DE'
	TIT1=TP+" "+MODULO
	TIT2="COMPLETA"
	TIT3="DE TODOS"
	lcabrm=100
	funcoes.cabr(produtos.textEdit,TIT1,TIT2,TIT3,len(resultado),lcabrm)
	linha='    CODIGO   BARRA      DESCRICAO____________________________________   RESUMIDA'
	produtos.textEdit.insertPlainText(linha+'\n')
	produtos.textEdit.insertPlainText(("-" * lcabrm)+'\n')
	for registro in resultado:
		produtos.textEdit.insertPlainText(registro['linha']+'\n')

	funcoes.filePreview(produtos.textEdit)


produtos.b_procurar.clicked.connect(procura_pro)
produtos.b_incluir.clicked.connect(inclui_pro)
produtos.b_alterar.clicked.connect(altera_pro)
produtos.b_excluir.clicked.connect(exclui_pro)
produtos.b_imprimir.clicked.connect(imprimir_pro)


produtos.show()
app.exec_()