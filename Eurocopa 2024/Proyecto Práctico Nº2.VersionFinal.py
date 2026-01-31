# Proyecto Práctico Nº2
# Andrés Jiménez C.I. 29.686.525
# Jesus Colombo C.I. 30.616.496
# Valentina Rodriguez C.I. 28.484.805
# Elena Sánchez C.I 31.873.786
# Sebastian Lopez C.I. 29.955.246

# Te queremos gabito <3 

# Activamos el paquete pandas para poder trabajar con dfFrames de csv y otros paquetes para poder graficar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify as sq
from scipy.stats import pearsonr
import statsmodels.api as sm
# Definimos los colores a utilizar en los gráficos
custom_palette = sns.color_palette(["#0c5254", "#1b6265", "#2a7376", "#398487", "#499598", "#59a6a9", "#69b7ba", "#79c8cb", "#89d9dc","#b3c4db"])
base_color = "#0c5254"

# Establecer el formato de los números flotantes para que no se muestren en notación científica
pd.options.display.float_format = '{:.2f}'.format

# Importamos el archivo euro2024_players.csv
df = pd.read_csv('euro2024_players.csv')

# Aquí podemos ver las primeras filas del DataFrame
pd.set_option('display.max_rows', None)
print(df.head())
print(df.info())

# Primero veremos unos datos que podrían sser relevantes para entender la df
# Contamos la categoría name para saber cuántos jugadores hay en total
players = df['Name'].count()
print(f"El número total de jugadores en el df es {players}")
# Contamos cuántos jugadores disitntos hay en la categoría name
unique_players = df['Name'].nunique()
print(f"El número de jugadores distintos en el df es {unique_players}")

# Limpiamos un poco el dataset
# Datos faltantes en el dataset
datos_faltantes = df.isnull().sum()
print("\nCantidad de datos faltantes en cada columna:")
print(datos_faltantes)
# Preferencia de pie
valores_foot = df['Foot'].unique()
print(f"\nValores únicos en la columna 'Foot': {valores_foot}")
# Jugadores con preferncia de pie "-"
jugadores_pie_desconocido = df[df['Foot'] == '-']
print(jugadores_pie_desconocido)
# Jugadores con preferencia de pie nula
no_foot = df[df['Foot'].isnull()]
print(f"Los jugadores cuya preferencia de pie no se conoce son {no_foot}")
# Cómo son pocos jugadores podemos completar la información manualmente
df.loc[df['Name'] == 'Lukas Cerv', 'Foot'] = 'right'
df.loc[df['Name'] == 'Matej Jurasek', 'Foot'] = 'left'
df.loc[df['Name'] == 'Mojmír Chytil', 'Foot'] = 'right'
df.loc[df['Name'] == 'Maximilian Entrup', 'Foot'] = 'both'
df.loc[df['Name'] == 'Thomas Kaminski', 'Foot'] = 'right'
df.loc[df['Name'] == 'Bogdan Racovițan', 'Foot'] = 'right'
# Verificamos que se hayan actualizado correctamente
print("\nActualización manual de la preferencia de pie:")
print(df.loc[df['Name'].isin(['Maximilian Entrup', 'Thomas Kaminski', 'Bogdan Racovițan', 'Lukas Cerv', 'Matej Jurasek', 'Mojmír Chytil']), ['Name', 'Foot']])

# Convertimos las columas adecuadas a tipo numérico
for col in ['Age', 'Height', 'Caps', 'Goals', 'MarketValue']:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Ahora con el data frame limpio podemos comenzar a responder las preguntas
# 1. ¿Cuál es el promedio de edad de los jugadores en el dataset?
promedio_edad = df['Age'].mean()
print(f"El promedio de edad de los jugadores es de {promedio_edad:.0f} años")

# Gráfico de distribución de edades
plt.figure(figsize=(10, 6))
sns.histplot(df['Age'], bins=20, kde=True, color=base_color)
plt.title('Distribución de Edades de los Jugadores')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.xticks(range(int(df['Age'].min()), int(df['Age'].max()) + 1))
plt.show()

# 2. ¿Cuántos jugadores hay en cada posición?
jugadores_por_posicion = df['Position'].value_counts()
print(f"\nJugadores por posición:\n{jugadores_por_posicion}")

# Gráfico de barras para jugadores por posición
plt.figure(figsize=(10, 6))
jugadores_por_posicion.plot(kind='bar', width=0.8, color=base_color)
plt.title('Jugadores por Posición')
plt.xlabel('Posición')
plt.ylabel('Número de Jugadores')
plt.xticks(rotation=45)
plt.show()

# 3. ¿Cuál es el club con más jugadores en el dataset?
max_jugadores = df['Club'].value_counts().max()
clubs_mas_jugadores = df['Club'].value_counts()[df['Club'].value_counts() == max_jugadores].index.tolist()
print(f"\nLos clubes con más jugadores son {' y '.join(clubs_mas_jugadores)}, con {max_jugadores} jugadores cada uno")

# Gráfica de barras top 10 clubes con más jugadores
top_10_clubs = df['Club'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_clubs.index, y=top_10_clubs.values)
plt.title('Top 10 clubes con más jugadores')
plt.xlabel('Club')
plt.ylabel('Cantidad de jugadores')
plt.xticks(rotation=45, ha='right') 
plt.show()

# 4. ¿Cuál es la altura promedio de los jugadores?
altura_promedio = df['Height'].mean()
print(f"\nLa altura promedio de los jugadores es {altura_promedio:.2f} cm")

plt.figure(figsize=(8, 6))
sns.histplot(df['Height'], bins=10, kde=True)
plt.title('Distribución de alturas de los jugadores')
plt.xlabel('Altura (cm)')
plt.ylabel('Frecuencia')
plt.show()

# 5. ¿Cuántos jugadores usan el pie izquierdo, derecho y ambos pies?
pie_uso = df['Foot'].value_counts()
print(f"\nJugadores por pie dominante\n{pie_uso}")

# Gráfico pie dominante por total de jugadores
# Calcular los porcentajes
pie_uso_percent = pie_uso / pie_uso.sum() * 100
labels = [f'{label}\n{value:.1f}%' for label, value in zip(pie_uso.index, pie_uso_percent)]
plt.figure(figsize=(10, 10))
sq.plot(sizes=pie_uso.values, label=labels, alpha=.8, color=sns.color_palette("Set3"))
plt.title('Uso del Pie Dominante')
plt.axis('off') 
plt.show()

# 6. ¿Cuál es el promedio de goles por jugador en cada club?
goles_por_club = df.groupby('Club')['Goals'].mean()
print(f"\nPromedio de goles por jugador en cada club:\n{goles_por_club}")

# Gráfica top 10 clubes con mayor promedio de goles por jugador
top_10_clubs_goals = goles_por_club.sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_clubs_goals.index, y=top_10_clubs_goals.values)
plt.title('Top 10 clubes con mayor promedio de goles por jugador')
plt.xlabel('Club')
plt.ylabel('Promedio de goles')
plt.xticks(rotation=45, ha='right')
plt.show()

# 7. ¿Cuál es el valor de mercado total de los jugadores de cada país?
valor_mercado_por_pais = df.groupby('Country')['MarketValue'].sum()
print(f"\nValor de mercado total por país:\n{valor_mercado_por_pais}")

#Arroje el top 3 países con el mayor y menor valor de mercado total
Top_3_paises_mayores = valor_mercado_por_pais.nlargest(3)
print(f"\nLos 3 países con el mayor valor de mercado total son:\n{Top_3_paises_mayores}")

Top_3_paises_menores = valor_mercado_por_pais.nsmallest(3)
print(f"\nLos 3 países con el menor valor de mercado total son:\n{Top_3_paises_menores}")   

# Gráfica top 10 países con mayor valor de mercado total
top_10_countries_market_value = valor_mercado_por_pais.sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_countries_market_value.index, y=top_10_countries_market_value.values)
plt.title('Top 10 países con mayor valor de mercado total')
plt.xlabel('País')
plt.ylabel('Valor de mercado total')
plt.xticks(rotation=45, ha='right')
plt.show()

# 8. ¿Cuál es el jugador más joven y el más viejo en el dataset?
jugador_mas_joven = df.loc[df['Age'].idxmin()]
jugador_mas_viejo = df.loc[df['Age'].idxmax()]
print(f"\nJugador más joven:\n{jugador_mas_joven}")
print(f"\nJugador más viejo:\n{jugador_mas_viejo}")

# 9. ¿Cuál es el promedio de partidos jugados (caps) por cada posición?
caps_por_posicion = df.groupby('Position')['Caps'].mean()
print(f"\nPromedio de partidos jugados por posición:\n{caps_por_posicion}")

# Gráfica promedio de caps por posición
plt.figure(figsize=(10, 6))
sns.barplot(x=caps_por_posicion.index, y=caps_por_posicion.values)
plt.title('Promedio de partidos jugados (caps) por posición')
plt.xlabel('Posición')
plt.ylabel('Promedio de caps')
plt.xticks(rotation=45, ha='right')
plt.show()

# 10. ¿Cuál es el promedio de valor de mercado de los jugadores que usan el pie izquierdo, derecho y ambos pies?
valor_mercado_por_pie = df.groupby('Foot')['MarketValue'].mean()
print(f"\nPromedio de valor de mercado por pie dominante:\n{valor_mercado_por_pie}")

# Gráfica promedio de valor de mercado por pie preferido
plt.figure(figsize=(8, 6))
sns.barplot(x=valor_mercado_por_pie.index, y=valor_mercado_por_pie.values)
plt.title('Promedio de valor de mercado por pie preferido')
plt.xlabel('Pie preferido')
plt.ylabel('Promedio de valor de mercado')
plt.show()

# 11. ¿Cuál es la relación entre la edad y el valor de mercado de los jugadores?
sns.scatterplot(x='Age', y='MarketValue', data=df)
plt.title('Relación entre Edad y Valor de Mercado')
plt.xlabel('Edad')
plt.ylabel('Valor de Mercado')
plt.show()

# 12. ¿Qué país tiene el promedio más alto de goles por jugador?
pais_promedio_goles = df.groupby('Country')['Goals'].mean()
pais_con_mas_goles = pais_promedio_goles.idxmax()
promedio_goles = pais_promedio_goles.max()
print(f"\nEl país con el promedio más alto de goles por jugador es {pais_con_mas_goles} con un promedio de {promedio_goles:.2f} goles por jugador")

# Gráfica top 10 países con mayor promedio de goles por jugador
top_10_countries_goals = pais_promedio_goles.sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_countries_goals.index, y=top_10_countries_goals.values)
plt.title('Top 10 países con mayor promedio de goles por jugador')
plt.xlabel('País')
plt.ylabel('Promedio de goles')
plt.xticks(rotation=45, ha='right')
plt.show()

# 13. ¿Cuál es el promedio de altura de los jugadores por posición y club?
altura_por_posicion_club = df.groupby(['Position', 'Club'])['Height'].mean()
print(f"\nPromedio de altura por posición y club:\n{altura_por_posicion_club}")

Promedio_altura_mayor = altura_por_posicion_club.idxmax()
print(f"\nEl promedio de altura más alto por posición y club es {Promedio_altura_mayor}")

Promedio_altura_menor = altura_por_posicion_club.idxmin()
print(f"\nEl promedio de altura más bajo por posición y club es {Promedio_altura_menor}")

# 13.1 Para ver mejor podemos agrupar en categorías más grandes 
 #Definimos las categorías de posición
definicion_posicion = {
    'Goalkeeper': 'Goalkeeper',
    'Attacking Midfield': 'Midfielder',
    'Central Midfield': 'Midfielder',
    'Defensive Midfield': 'Midfielder',
    'Left Midfield': 'Midfielder',
    'Right Midfield': 'Midfielder',
    'Left Winger': 'Forward',
    'Right Winger': 'Forward',
    'Centre-Forward': 'Forward',
    'Second Striker': 'Forward',
    'Left-Back': 'Defender',
    'Right-Back': 'Defender',
    'Centre-Back': 'Defender',
    'Sweeper': 'Defender'
}
df['PositionCategory'] = df['Position'].map(definicion_posicion)    
print(f"\nCategorías de posición:\n{df['PositionCategory'].value_counts()}")

# Gráfico de barras para las categorías de posición
plt.figure(figsize=(10, 6))
sns.countplot(x='PositionCategory', data=df, palette=custom_palette)
plt.title('Categorías de Posición')
plt.xlabel('Categoría')
plt.ylabel('Número de Jugadores')
plt.show()

# 13.1.1. ¿Cuál es el promedio de altura de los jugadores por categoría de posición?
altura_por_categoria_posicion = df.groupby('PositionCategory')['Height'].mean()
print(f"\nPromedio de altura por categoría de posición:\n{altura_por_categoria_posicion}")

# Grafico de barras para las categorías de posición con respeecto a la altura
plt.figure(figsize=(10, 6))
sns.boxplot(x='PositionCategory', y='Height', data=df, palette=custom_palette)
plt.title('Distribución de Altura por Categoría de Posición')
plt.xlabel('Categoría')
plt.ylabel('Altura (cm)')
plt.show()


# 13.1.2 Promedio de altura por club de la posición de portero
altura_porteros = df[df['PositionCategory'] == 'Goalkeeper'].groupby('Club')['Height'].mean()
print(f"\nPromedio de altura por club de porteros:\n{altura_porteros}")

# 13.1.3 Promedio de altura por club de la posición de defensor
altura_defensores = df[df['PositionCategory'] == 'Defender'].groupby('Club')['Height'].mean()
print(f"\nPromedio de altura por club de defensores:\n{altura_defensores}")

# 13.1.4 Promedio de altura por club de la posición de mediocampista
altura_mediocampistas = df[df['PositionCategory'] == 'Midfielder'].groupby('Club')['Height'].mean()
print(f"\nPromedio de altura por club de mediocampistas:\n{altura_mediocampistas}")

# 13.1.5 Promedio de altura por club de la posición de delantero
altura_delanteros = df[df['PositionCategory'] == 'Forward'].groupby('Club')['Height'].mean()
print(f"\nPromedio de altura por club de delanteros:\n{altura_delanteros}")

# 14. ¿Cuál es la correlación entre el número de partidos jugados y el número de goles?
correlacion_caps_goles = df['Caps'].corr(df['Goals'])
print(f"\nLa correlación entre partidos jugados y goles es de {correlacion_caps_goles:.2f}")

# 15. ¿Cuál es el club con el valor de mercado promedio más alto de sus jugadores?
club_valor_mercado_promedio = df.groupby('Club')['MarketValue'].mean()
club_mayor_valor = club_valor_mercado_promedio.idxmax()
mayor_promedio_valor = club_valor_mercado_promedio.max()
print(f"\nEl club con el valor de mercado promedio más alto es {club_mayor_valor} con un valor promedio de {mayor_promedio_valor:.2f}")

#EXTRA 1: Relación entre el valor de mercado y los goles anotados.
# Gráfico de dispersión con línea de regresión
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='MarketValue', y='Goals', scatter_kws={'color': '#1b6265', 'alpha': 0.6}, line_kws={'color': 'red'})

plt.title('Relación entre Valor de Mercado y Goles Anotados (Línea de Regresión)', fontsize=16)
plt.xlabel('Valor de Mercado (en millones de euros)', fontsize=12)
plt.ylabel('Goles Anotados', fontsize=12)
plt.grid(True)
plt.show()
# Calcular la correlación
correlation, p_value = pearsonr(df['MarketValue'], df['Goals'])
print(f"Correlación entre Valor de Mercado y Goles: {correlation:.2f}")
print(f"p-value: {p_value:.4f}")

# EXTRA 2. Cuál es la relación de los mejor jugadores basados en sus datos de goals, marketvalue y caps, existe un patrón entre las posiciones y/o edades de los mismos?
# 1. Identificar a los 100 Mejores Jugadores
# Normalizar las columnas para combinarlas (evitar que una variable domine por su escala)
df['Normalized_MarketValue'] = (df['MarketValue'] - df['MarketValue'].min()) / (df['MarketValue'].max() - df['MarketValue'].min())
df['Normalized_Goals'] = (df['Goals'] - df['Goals'].min()) / (df['Goals'].max() - df['Goals'].min())
df['Normalized_Caps'] = (df['Caps'] - df['Caps'].min()) / (df['Caps'].max() - df['Caps'].min())

# Crear una métrica combinada (suma ponderada)
df['Combined_Score'] = 0.4 * df['Normalized_MarketValue'] + 0.4 * df['Normalized_Goals'] + 0.2 * df['Normalized_Caps']

# Ordenar por la métrica combinada y seleccionar los 100 mejores jugadores
top_100_players = df.sort_values(by='Combined_Score', ascending=False).head(100)

# Ver los 100 mejores jugadores
print(top_100_players[['Name', 'Position', 'Age', 'MarketValue', 'Goals', 'Caps']])

# 2. Analizar la Relación entre Goals, MarketValue y Caps
# a) Matriz de Dispersión
# Pairplot para visualizar las relaciones
sns.pairplot(top_100_players[['MarketValue', 'Goals', 'Caps']], diag_kind='kde', palette=custom_palette)
plt.suptitle('Relaciones entre MarketValue, Goals y Caps (Top 100 Jugadores)', y=1.02)
plt.show()
# Calcular la matriz de correlación
correlation_matrix = top_100_players[['MarketValue', 'Goals', 'Caps']].corr()

# b) Heatmap de correlación
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap=sns.light_palette(base_color, as_cmap=True), fmt='.2f')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.title('Matriz de Correlación entre MarketValue, Goals y Caps (Top 100 Jugadores)')
plt.show()

# c) Correlaciones individuales
# Correlación entre MarketValue y Goals
cor_mv_goals, _ = pearsonr(top_100_players['MarketValue'], top_100_players['Goals'])
print(f"Correlación entre MarketValue y Goals: {cor_mv_goals:.2f}")

# Correlación entre MarketValue y Caps
cor_mv_caps, _ = pearsonr(top_100_players['MarketValue'], top_100_players['Caps'])
print(f"Correlación entre MarketValue y Caps: {cor_mv_caps:.2f}")

# Correlación entre Goals y Caps
cor_goals_caps, _ = pearsonr(top_100_players['Goals'], top_100_players['Caps'])
print(f"Correlación entre Goals y Caps: {cor_goals_caps:.2f}")

# 3. Analizar Patrones por Posición y Edad
# Distribucion por posicion
plt.figure(figsize=(10, 6))
sns.countplot(data=top_100_players, x='Position', palette=custom_palette)
plt.title('Distribución de Posiciones entre los Top 100 Jugadores', fontsize=16)
plt.xlabel('Posición', fontsize=12)
plt.ylabel('Número de Jugadores', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Boxplot de edad por posición
plt.figure(figsize=(12, 8))
sns.boxplot(data=top_100_players, x='Position', y='Age', palette=custom_palette)
plt.title('Distribución de Edades por Posición (Top 100 Jugadores)', fontsize=16)
plt.xlabel('Posición', fontsize=12)
plt.ylabel('Edad', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Calcular la media de edad por posición
edad_por_posicion = top_100_players.groupby('Position')['Age'].mean().sort_values(ascending=False)
print(edad_por_posicion)

# Gráfico de barras para la media de edad por posición
plt.figure(figsize=(10, 6))
edad_por_posicion.plot(kind='bar', color=base_color)
plt.title('Media de Edad por Posición (Top 100 Jugadores)', fontsize=16)
plt.xlabel('Posición', fontsize=12)
plt.ylabel('Edad Promedio', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

#4. Segmentar por Edad y Posición
# Filtrar jugadores jóvenes
jovenes = top_100_players[top_100_players['Age'] < 25]

# Ver la distribución de posiciones entre jugadores jóvenes
plt.figure(figsize=(10, 6))
sns.countplot(data=jovenes, x='Position', palette=custom_palette)
plt.title('Distribución de Posiciones entre Jugadores Jóvenes (<25 años)', fontsize=16)
plt.xlabel('Posición', fontsize=12)
plt.ylabel('Número de Jugadores', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Filtrar jugadores mayores
mayores = top_100_players[top_100_players['Age'] > 30]

# Ver la distribución de posiciones entre jugadores mayores
plt.figure(figsize=(10, 6))
sns.countplot(data=mayores, x='Position', palette=custom_palette)
plt.title('Distribución de Posiciones entre Jugadores Mayores (>30 años)', fontsize=16)
plt.xlabel('Posición', fontsize=12)
plt.ylabel('Número de Jugadores', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()