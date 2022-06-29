import mysql.connector

host1 = 'mysql-81434-0.cloudclusters.net'
port1 = 13003
user1 = 'marcos6533'
passwd1 = 'marcos12'       
db1 = 'votaciones'     
connect= mysql.connector.connect(host=host1, port=port1, user=user1, passwd=passwd1, db=db1)

  
def verificar(cedula):
        host1 = 'mysql-81434-0.cloudclusters.net'
        port1 = 13003
        user1 = 'marcos6533'
        passwd1 = 'marcos12'       
        db1 = 'votaciones'     
        connect= mysql.connector.connect(host=host1, port=port1, user=user1, passwd=passwd1, db=db1)

  
        cursor = connect.cursor()           
        cursor.execute("select cedula from usuarios")
        verificar=False     
        for fila in cursor:
            if fila[0] == cedula:
                verificar = True
        if verificar == True:
            comprobar = True
        else:
            comprobar = False
        connect.close()
        return comprobar
    
    
def Numero_personas_votaron():
    host1 = 'mysql-81434-0.cloudclusters.net'
    port1 = 13003
    user1 = 'marcos6533'
    passwd1 = 'marcos12'       
    db1 = 'votaciones'     
    connect= mysql.connector.connect(host=host1, port=port1, user=user1, passwd=passwd1, db=db1)

  
    cursor = connect.cursor()         
    cursor.execute("select voto from usuarios") 
    si_voto=0     
    for fila in cursor:
        if fila[0]=='Si':
            si_voto+=1
       
    return si_voto            


def Numero_personas_no_votaron():
    host1 = 'mysql-81434-0.cloudclusters.net'
    port1 = 13003
    user1 = 'marcos6533'
    passwd1 = 'marcos12'       
    db1 = 'votaciones'     
    connect= mysql.connector.connect(host=host1, port=port1, user=user1, passwd=passwd1, db=db1)

  
    cursor = connect.cursor() 
    cursor.execute("select voto from usuarios") 
    no_voto=0      
    for fila in cursor:
        if fila[0]=='No':
            no_voto+=1
         
    return no_voto   

def Numero_personas_habilitas():
    shost1 = 'mysql-81434-0.cloudclusters.net'
    port1 = 13003
    user1 = 'marcos6533'
    passwd1 = 'marcos12'       
    db1 = 'votaciones'     
    connect= mysql.connector.connect(host=host1, port=port1, user=user1, passwd=passwd1, db=db1)

    
    cursor = connect.cursor() 
    cursor.execute("select voto from usuarios") 
    num_personas=0      
    for fila in cursor:
        num_personas+=1
       
    return num_personas    
