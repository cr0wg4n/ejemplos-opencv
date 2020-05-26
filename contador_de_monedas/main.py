import cv2
import shutil
import os
import numpy as np
import random



class Moneda():
  def __init__(self, nombre, valor, diametro, tolerancia):
    self.nombre = nombre
    self.valor = valor
    self.diametro = diametro
    self.tolerancia = tolerancia

# Relación de tamaños
# 2Bs. -> 290 mm 
# 1Bs. -> 270 mm 
# 0,50Bs. -> 240 mm 
class Clasificador():
  def __init__(self, tolerancia=0.035):
    self._1bs = 270
    self._2bs = 290
    self._050bs = 240
    self.monedas = [Moneda("1bs",1,self._1bs,0),
                    Moneda("2bs",2,self._2bs,0),
                    Moneda("0.50bs",0.50,self._050bs,0),
                  ]
    self.tolerancia = tolerancia
    self.memoria = []

  def extraer_relaciones(self):
    relaciones = []
    for i in range(len(self.monedas)):
      for j in (range(i+1, len(self.monedas))):
        if (self.monedas[i].valor > self.monedas[j].valor):
          moneda_g = self.monedas[i]
          moneda_p = self.monedas[j]
        else: 
          moneda_p = self.monedas[i]
          moneda_g = self.monedas[j]
        relaciones.append({
          "constante": moneda_p.diametro / moneda_g.diametro,
          "mayor_valor": moneda_g.valor,
          "menor_valor": moneda_p.valor,
        })
    return relaciones

  def extraer_relaciones_genericas(self, arreglo, key):
    relaciones = []
    for i in range(len(arreglo)):
      for j in (range(i+1, len(arreglo))):
        if(arreglo[i][key] > arreglo[j][key]):
          moneda_g = arreglo[i]
          moneda_p = arreglo[j]
        else:
          moneda_g = arreglo[j]
          moneda_p = arreglo[i]
        relaciones.append({
          "constante": moneda_p[key] / moneda_g[key],
          "mayor_valor": moneda_g[key],
          "menor_valor": moneda_p[key],
        })
    return relaciones
          
  def aproximacion(self, radios):
    posibilidades = []
    agrupado = self.agrupar(radios, "radio")
    new_radios = []
    numeros_de_monedas_grupo = []

    for grupo in agrupado:
      new_radios.append(grupo[0])
      numeros_de_monedas_grupo.append(len(grupo))

    if (len(new_radios) > 1):
      relaciones_internas = self.extraer_relaciones()
      relaciones_externas = self.extraer_relaciones_genericas(new_radios, "radio")
      valores = []
      for relacion in relaciones_internas:
        for relacion_externa in relaciones_externas:
          constante = abs(relacion["constante"] - relacion_externa["constante"])
          if constante <= self.tolerancia:
            posibilidades.append({
              "interno": relacion,
              "externo": relacion_externa,
              "diferencia": constante
            })
            mayor_valor = { 
              "valor": relacion["mayor_valor"],
              "radio": relacion_externa["mayor_valor"]
            }
            menor_valor = { 
              "valor": relacion["menor_valor"],
              "radio": relacion_externa["menor_valor"]
            }
            if mayor_valor not in valores:
              valores.append(mayor_valor)
            if menor_valor not in valores:
              valores.append(menor_valor)
      total = 0
      for valor in valores:
        numero_de_monedas = numeros_de_monedas_grupo[self.esta_en_grupo(agrupado, valor["radio"])]
        valor_moneda = valor["valor"]
        total = total + numero_de_monedas*valor_moneda
        print("Se tiene:",numero_de_monedas,"moneda(s) de",valor_moneda,"Bs.")
        self.memoria.append({
          "radio": valor["radio"],
          "valor": valor["valor"]
        })
      print("Total:", total, "Bs.")
    else:
      total = 0
      for radio in radios:
        memoria = self.utilizar_memoria(radio["radio"])
        print("Se tiene:",1,"moneda de",memoria["valor"],"Bs.")
        total = total + 1 * memoria["valor"]
      print("Total:", total, "Bs.")
    print("\n\n")
    
  def esta_en_grupo(self, matriz, valor, key="radio"):
    for i, item in enumerate(matriz):
      for j in item:
        if (j[key]==valor):
          return i
    return -1

  def agrupar(self, arr, key):
    arreglo = arr.copy()
    grupos = []
    i = 0
    while(len(arreglo) != 0):
      grupo = []
      inicial = arreglo.pop(i)
      grupo.append(inicial)
      j=0
      while True:
        if (j == len(arreglo)):
          break
        if (inicial[key] < arreglo[j][key]):
          constante = inicial[key] / arreglo[j][key]
        else:
          constante = arreglo[j][key] / inicial[key]
        diferencia = 1 - constante
        if (diferencia <= self.tolerancia):
          grupo.append(arreglo.pop(j))
          j = j-1
        j = j + 1 
      grupos.append(grupo)
    return grupos
          

  def utilizar_memoria(self, valor):
    print("Usando memoria...")
    for dato in self.memoria:
      diferencia = self.extraer_dif(valor,dato["radio"])
      if (diferencia <= self.tolerancia):
        return dato
    return []
  
  def extraer_dif(self, valor_a, valor_b):
    if (valor_a < valor_b):
      constante = valor_a  / valor_b
    else: 
      constante = valor_b / valor_a
    diferencia = 1 - constante
    return diferencia

class ModenasImg():
  def __init__(self, ruta, nombre, valor_total):
    self.nombre = nombre
    self.ruta = ruta
    self.valor_total = valor_total
    self.data = self.lectura()
  
  def redimencion (self, porcentaje):
    h = int(self.data.shape[0] * (porcentaje / 100))
    w = int(self.data.shape[1] * (porcentaje / 100))
    return cv2.resize(self.data, (w, h))

  def lectura (self):
    return cv2.imread(self.ruta_completa())

  def escritura (self, ruta, nueva_img, etiqueta="_"):
    if os.path.exists(self.ruta_completa(ruta)):
      self.nombre = etiqueta + self.nombre
    cv2.imwrite(self.ruta_completa(ruta), nueva_img)

  def ruta_completa(self, ruta=None):
    if ruta:
      return os.path.join(ruta, self.nombre)
    else:
      return os.path.join(self.ruta, self.nombre)

  def crear_imagen_vacia(self, imagen):
    h, w, c = imagen.shape
    return np.zeros((h,w,c), np.uint8)
  
def main():
  clasificador = Clasificador()
  ruta_salida = "salida"
  ruta = "datos"
  if os.path.exists(ruta_salida):
    shutil.rmtree(ruta_salida)
  os.mkdir(ruta_salida)
  imagenes = []
  imagenes.append(ModenasImg(ruta,"1_5bs.jpg",1.5))
  imagenes.append(ModenasImg(ruta,"1_5bs2.jpg",1.5))
  imagenes.append(ModenasImg(ruta,"1_bs.jpg",1))
  imagenes.append(ModenasImg(ruta,"2_5bs.jpg",2.5))
  imagenes.append(ModenasImg(ruta,"2_bs.jpg",2))
  imagenes.append(ModenasImg(ruta,"3_5bs.jpg",3.5))
  imagenes.append(ModenasImg(ruta,"3_5bs2.jpg",3.5))
  imagenes.append(ModenasImg(ruta,"3_bs.jpg",3))
  imagenes.append(ModenasImg(ruta,"4_bs.jpg",4))
  imagenes.append(ModenasImg(ruta,"4_bs2.jpg",4))

  for imagen in imagenes:
    print("Evaluando: Imagen",imagen.nombre,"de",imagen.valor_total,"Bs. en total")
    original_img = imagen.redimencion(20)

    copia_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    
    contador_blur = 4
    for i in range(contador_blur):
      copia_img = cv2.GaussianBlur(copia_img,(5,5),cv2.BORDER_REFLECT)
    # imagen.escritura(ruta_salida, copia_img, "blur")

    threshold = 45
    copia_img = cv2.Canny(copia_img, threshold, threshold*3)
    # imagen.escritura(ruta_salida, copia_img, "canny")

    contornos, jerarquia =  cv2.findContours(copia_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contornos_img = original_img.copy()
    radios = []
    for indice, contorno in enumerate(contornos):
      color = (0,255,255)
      cv2.drawContours(contornos_img, contornos, indice, color, 2)
      (x,y),radio = cv2.minEnclosingCircle(contorno)
      radios.append({
        "radio": radio,
        "centro_x": int(x),
        "centro_y": int(y)
      })

    clasificador.aproximacion(radios)
    imagen.escritura(ruta_salida, contornos_img, "contornos")

if __name__ == "__main__":
    main()



