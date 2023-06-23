#Modelo Tuplas

import random

relaciones = [
    ('Principio de Contradicción', 'Sentencia 338/2018'),
    ('Juez de Amparo', 'Tribunal Colegiado'),
    ('Auto de Vinculación a Proceso', 'Juez de Control'),
    ('Organo Jurisdiccional', 'Juez de Control'),
    ('Juzgado de Control', 'Sentencia 338/2018'),
    ('Juzgado de Distrito', 'Sentencia 338/2018'),
    ('Norma Convencional que contempla justa indemnizacion', 'Sentencia 423/2019'),
    ('Autoridad Jurisdiccional', 'Suprema Corte de Justicia de la Nación'),
    ('Organo Jurisdiccional', 'Juez de Amparo'),
    ('Norma Convencional que contempla justa indemnizacion', 'Artículo 63.1 Convención Americana sobre Derechos Humanos'),
    ('Juez de Amparo', 'Juzgado de Distrito'),
    ('Tribunal Colegiado', 'Sentencia 338/2018'),
    ('Norma Convencional que contempla justa indemnizacion', 'Norma Convencional'),
    ('Prisión Preventiva Oficiosa', 'Órgano Jurisdiccional'),
    ('Autoridad Jurisdiccional', 'Órgano Jurisdiccional')
]

elemento1, elemento2 = random.sample(set([relacion[0] for relacion in relaciones]), 2)
elementos_relacionados = []

for relacion in relaciones:
    if relacion[0] == elemento1 or relacion[0] == elemento2:
        elementos_relacionados.append(relacion[1])
    if relacion[1] == elemento1 or relacion[1] == elemento2:
        elementos_relacionados.append(relacion[0])

elemento3 = random.choice(elementos_relacionados)

print("los elementos input ","(",elemento1,")", "(",elemento2,")")
print("los elementos output ","(",elemento1,")","(",elemento2,")","(",elemento3,")")