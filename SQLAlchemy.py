#Para contal la cantidad de filas -------------------------

#returned = session.query(get_client).count()

#print(returned)

#Para agregar--------------------

#user1 = get_client(id=8,name="Cesar Aguirre")

#session.add(user1)

#session.commit()

#Para consultar 

#returned = session.query(get_client).filter(get_client.id >= 3)


#for user in returned:
    #print(user.name)


#Obtener el primer valor dnde la consulta sea igual a tal valor 

#returned = session.query(get_client_db).filter(get_client_db.contract == '0000000209').first()

#print(returned.name_1)

#Y PARA MODIFICAR EL VALOR 

#returned.name_1 = 'YUGLENIS'
#session.add(returned)
#session.commit()