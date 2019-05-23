import socket, select

#Funcao que envia a mensagem para todos os usuarios conectados
def enviar_mensagem (sock, message):
	for socket in conectados:
		if socket != server_socket and socket != sock : #nao manda a mensagem para o proprio servidor
			socket.send(message)

if __name__ == "__main__":

	#*******INICIA O SERVIDOR***********#
	nome_usuario={}
	conectados = [] #lista dos usuarios conectados
	nome=""
	buffer = 4096
	port = 5001
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("localhost", port))
	server_socket.listen(5) # ate 5 usuarios simultaneos
	conectados.append(server_socket)
	print "Servidor ligado!!!" 
	#***********************************#

	while 1:
		rList,wList,error_sockets = select.select(conectados,[],[]) #rastreia os usuarios conectados para poder mandar a mensagem

		for sock in rList:
			if sock == server_socket: 
			#Nova conexao. Usuario novo.
				sockfd, addr = server_socket.accept()
				nome=sockfd.recv(buffer)
				conectados.append(sockfd)
                
				nome_usuario[addr]=nome

				#printa para o servidor
				print "Client (%s, %s) connected" % addr," [",nome_usuario[addr],"]"
				#printa para o usuario que entrou
				sockfd.send("Oi. Digite 'sair' para encerrar a conexao\n")
				#printa para os usuarios conectados
				enviar_mensagem(sockfd, nome+" entrou no chat\n")

			else:	
			#Mensagem de um usuario ja conectado.
	
				data1 = sock.recv(buffer)
				data=data1[:data1.index("\n")]
				i,p=sock.getpeername()
				if data == "sair":
				#encerra a conexao a pedido do usuario
					msg=" "+nome_usuario[(i,p)]+" saiu do chat\n"
					enviar_mensagem(sock,msg)
					#printa para o servidor que o usuario deslogou
					print "Usuario (%s, %s) saiu" % (i,p)," [",nome_usuario[(i,p)],"]\n"
					del nome_usuario[(i,p)]
					conectados.remove(sock) #remove o usuario da lista dos usuarios ativos
					sock.close() #fecha a conexao
					continue

				else:
					msg= nome_usuario[(i,p)]+": "+data+"\n"
					enviar_mensagem(sock,msg)
            
	#desliga o servidor
	server_socket.close()

