"""
    it is a code only used in qgis for now
"""

#TODO
# Necessary test and refactor this code


nome_da_camada = 'perimetro_rep'

# Encontra a camada pelo nome
layer = QgsProject.instance().mapLayersByName(nome_da_camada)[0]

# Inicia a edição
layer.startEditing()

# Adiciona um novo campo para a área em hectares
nome_campo = 'Area_ha3'
if layer.fields().indexFromName(nome_campo) == -1:  # Verifica se o campo já existe
    layer.dataProvider().addAttributes([QgsField(nome_campo, QVariant.Double)])
    layer.updateFields()

# Index do novo campo
idx = layer.fields().indexFromName(nome_campo)

# Verifica se a camada é do tipo polígono
if not layer.geometryType() == QgsWkbTypes.PolygonGeometry:
    print("A camada selecionada não é uma camada de polígono.")
else:
    # Itera sobre as feições da camada
    for feature in layer.getFeatures():
        # Calcula a área em hectares (1 ha = 10.000 m²)
        area_hectares = round(feature.geometry().area() / 10000, 2)
        # Atualiza a feição com a área calculada
        layer.changeAttributeValue(feature.id(), idx, area_hectares)

# Salva as alterações
layer.commitChanges()
