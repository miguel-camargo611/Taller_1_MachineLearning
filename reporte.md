# Reporte Ejecutivo: Clustering de Actividad Sísmica en Colombia

## Resumen
Este estudio aborda la caracterización de la identificación de zonas sísmicas en Colombia mediante el uso de técnicas de aprendizaje no supervisado (K-Means). El territorio colombiano, al ser un nodo de convergencia tectónica entre las placas de Nazca, Caribe y Sudamérica, presenta una complejidad que dificulta la zonificación manual basada únicamente en criterios políticos.

Utilizando un dataset de **2,588** registros (2010-2026) y estandarizando las variables del mismo, se implementó un modelo de clustering tridimensional (Latitud, Longitud, Profundidad). Los resultados revelan 5 regiones sísmicas críticas con firmas estadísticas únicas, permitiendo identificar no solo zonas de recurrencia, sino también deficiencias de monitoreo instrumental.

## Metodología (CRISP-DM)
1.  **Business Understanding**: Se definió el objetivo de automatizar la identificación de zonas sísmicas para optimizar monitoreos del SGC y la UNGRD. Revisando en la literatura, se encontro que colombia posee 5 grandes regiones sismicas que corresponden a la zona de subduccion en el pacifico, la zona de subduccion en el caribe, el nudo de bucaramanga, zona andina y la zona volcanica.
2.  **Data Understanding**: Realizamos un EDA que identificó una distribución bimodal de profundidad, que junto a los scatter plots nos permitió identificar la presencia de nudos sísmicos. **Consideración importante sobre los datos**: Si incluimos todos los sismos desde magnitud 1.5, estamos metiendo datos que a veces las estaciones no captan bien (sensores lejos, ruido ambiental). Ese "microrruido" ensucia visualmente el clúster e introduce artefactos. Entonces decidimos filtrar esos datos quedándonos exclusivamente con los **2,588** eventos de mayor magnitud. Al eliminar el ruido, las estructuras tectónicas (como la subducción o el nido profundo) se delimitan con mucha mayor claridad.
3.  **Data Preparation**: Normalizamos magnitudes siguiendo la metodología de Scordilis (2006), pues la varaible de magnitud mostraba originalmente distintas unidades y aplicamos **StandardScaler** para equilibrar la influencia de la profundidad frente a las coordenadas geográficas.
4.  **Modeling**: Evaluamos modelos de K=2 a K=10. El método del codo confirmo que un **K=5** ofrece el balance óptimo entre separabilidad estadística e interpretabilidad geológica. Si bien el de silueta, arrojo un K=6 como optimo, al analizar esa clusterizacion, se observo que no era tan coherente con la realidad geologica del pais.
5.  **Evaluation**: Se analizaron los perfiles de cada clúster, validando que el modelo captura correctamente los fenómenos de subducción y la sismicidad reportada en la literatura

## Resultados 
### Perfil de los Clústeres
El modelo identificó cinco clústeres principales:
-   **Santanderes (Nido de Bucaramanga)**: Sismicidad intermedia a profunda de alta densidad espacial, asociada al fenómeno del Nido de Bucaramanga.
-   **Pacífico Sur (Tumaco)**: Zona de subducción activa caracterizada por sismos intermedios a profundos y los mayores valores de magnitud promedio.
-   **Sur / Ecuador**: Zona de transición tectónica con mezcla de sismicidad superficial e intermedia asociada al contacto Nazca–Suramérica.
- **Llanos y piedemonte**: Sismicidad predominantemente superficial y de menor magnitud promedio, posiblemente asociada a fallamiento cortical e intraplaca.
- **Centro y pacifico norte**: Zona caracterizada por sismicidad superficial de alta frecuencia, asociada a fallamiento cortical activo y segmentación de la subducción.

### Hallazgos Claves

Es interesante la relacion que hay entre profundidad y magnitud del sismo, por ejemplo, sismos poco profundos tienden a ser de mayor magnitud, mientras que sismos profundos tienden a ser de menor magnitud.

Se detectaron las principales zonas sismicas del pais, como el nido de bucaramanga y la zona de subduccion en el pacifico

### ¿Algún cluster captura los sismos de mayor magnitud?
Sí, el **Clúster  (pacifico sur)** Concentra una densidad crítica de eventos de magnitud intermedia. Por su parte los clusters **sur/ecuador** y **santander/bucaramanga** concentra la amyoria de sismos, siendo la region mas activa del pais.

## Impacto del Scaling
El escalado de variables fue el paso más crítico. Al normalizar Latitud, Longitud y Profundidad, el algoritmo K-Means pudo identificar agrupaciones basadas en la forma real de las fallas terrestres, y no simplemente por la magnitud numérica de los kilómetros de profundidad.

## Recomendaciones para el SGC
Utilizando el **Snake Plot** de diagnóstico, recomendamos:
-   **Prioridad Alta (Pacífico Sur)**: Presenta las mayores magnitudes Mw pero un Gap azimutal elevado. Se requiere instalar más estaciones mas repartidas y alejadas entre si, para mejorar la precision de la localizacion de los sismos. Tal vez incluso estaciones moviles en boyas.
-   **Optimización (Piedemonte)**: Es la zona con mejor cobertura (NST alto), sirviendo como referencia para la calibración de la red nacional.

## Conclusiones
-   **K-Means** es excelente para encontrar nidos y zonificar grandes volúmenes de datos, pero **no puede** predecir sismos ni identificar fallas individuales con precisión milimétrica (ya que asume formas geométricas simples).
-   La automatización reduce el sesgo humano en la zonificación, permitiendo que la UNGRD planee por riesgo geológico real y no por fronteras departamentales.

## Referencias
-   **USGS Earthquake Catalog**: Datos originales de eventos sísmicos.
-   **Scordilis, E. M. (2006)**: Empirical relations converting various magnitude scales to Mw.
- **UNGRD**.(2025). Informe cierre ejecución Presupuestal
- **Servicio Geológico Colombiano**.(2025). Informe de rendicion de cuentas 2025.
- **Servicio Geológico Colombiano**.(2026). Amenaza sismica