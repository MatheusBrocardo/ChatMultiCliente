import socket, select, string, sys

def display() :
	you=""
	sys.stdout.write(you)
	sys.stdout.flush()

def main():

    if len(sys.argv)<2:
        host = "localhost" #localhost como padrao caso o usuario nao informe o endereco do servidor

    port = 5001
    
    #O usuario entra o nome
    name=raw_input("Insira um nome de usuario:\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    #faz a conexao com o servidor
    try :
        s.connect((host, port))
    except :
        print "Host nao encontrado!!!!"
        sys.exit()

    #*********CONECTADO***********#
    s.send(name)
    display()
    while 1:
        socket_list = [sys.stdin, s]
        rList, wList, error_list = select.select(socket_list , [], []) #busca os usuarios conectados
        
        for sock in rList:
            if sock == s: 
	    #a mensagem veio do servidor
                data = sock.recv(4096)
                if not data :
                    print 'Voce saiu do chat com sucesso!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display()
        
            else :
	    #a mensagem veio de um usuario
                msg=sys.stdin.readline()
                s.send(msg)
                display()
    #*****************************#

if __name__ == "__main__":
    main()
