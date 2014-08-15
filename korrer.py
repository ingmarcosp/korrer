print ""
print "Korrer, un programa que facilita el calculo y registro de tiempos de",
print " carreras o entrenamientos_"
print ""
print "Para empezar debes introducir algunos datos asi que ten a mano el cronometro"
print ""

#carrera o entrenamiento
cor=raw_input("ingresa (C) si fue una carrera o (E) si fue un entrenamiento: ")
cor = cor.upper()

if cor==str("C" ):
	cor=str("Carrera")
else:
	if cor==str("E" ):
		cor=str("Entrenamiento")


#Fecha
fecha=raw_input("Ingresa la fecha (dd/mm/aa): ")
print ""

#Diempo
hs= float(raw_input("Ingresa las horas: "))
minu= float(raw_input("Ingresa los minutos: "))
seg= float(raw_input("Ingresa los segundos: "))

# el problema aca es que primero no se ingresa ninguna cadena en el raw_input,
# y no puede convertirlo a nada, entonces
# la funcion de abajo no sirve,
if hs and minu and seg:
    print""
else:
    hs and minu and seg == 0

#Distancia
km= float(raw_input("ingresa los kilometros:"))
mt= float(raw_input("Ingresa los metros:"))

print ""
print "Tiempo el tiempo es", int(hs),":",int(minu),":",int(seg),

#Ahora empieza la cosa de verdad, no te asuste por lo que veas a continuacion,
#Si sabes una forma mas simple de hacerlo, como es GPL manos a la obra,
#recuerda yo ni siquiera se usar python

#Calculos

#Velocidad Promedio
tiempo_hs= hs+round(((minu+round((seg/60), 3))/60), 3)                   #tiempo en horas
distancia_km= km+round((mt/1000), 3)                                     #distancia en Kilometros
velpro= round(float(distancia_km/tiempo_hs), 3)                          #kilometros por hora


print ""
print "la velocidad promedio es:",velpro,"Km/hs"

#Minutos y Kilometros totales

minu_t= (hs*60)+minu+round((seg/60), 3)                         #minutos totales
km_t= km+round((mt/1000), 3)                                    #Kilometros totales

#Ritmo de Carrera
ritmo= round(minu_t/km_t, 3)

#Ritmo de carrera en hh:mm:ss
ritmo_sd= int(ritmo)                                           #ritmo sin decimales
ritmo_seg=ritmo-float(ritmo_sd)                                #decimales del ritmo en minutos
minuaseg=ritmo_seg*60                                          #decimales del ritmo de minutos a segundos

print""
print "El Ritmo de carrera fue de:",ritmo_sd,":",minuaseg,"min/km"

#escribir en un archivo

korrer = open('korrer.csv', "a")
korrer.write(fecha)
korrer.write(",")
korrer.write(cor)
korrer.write(",")
korrer.write(str(distancia_km))
korrer.write(" Km,")
korrer.write(str(hs))
korrer.write(":")
korrer.write(str(minu))
korrer.write(":")
korrer.write(str(seg))
korrer.write(",")
korrer.write(str(ritmo_sd))
korrer.write(":")
korrer.write(str(minuaseg))
korrer.write(",")
korrer.write(str(velpro))
korrer.write("\n")
korrer.close()

