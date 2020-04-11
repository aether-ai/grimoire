import glob as glob

spells = glob.glob("spells/**/*.py")
dict_string = "REGISTERED_SPELLS = dict("
for spell in spells:
    spell_string = spell.split("/")
    spell_type = spell_string[1]
    spell_name = spell_string[2].split(".py")[0]
    #import all spells
    
    imp_statement = "from ." + spell_type + "."+ spell_name + " import spell as "+spell_name
    #print(imp_statement)
    exec(imp_statement)
    # REGISTERED_SPELLS[spell_name] = spell_name
    dict_string+=spell_name+"="+spell_name+",\n"

dict_string+=")"

#print(dict_string)
exec(dict_string)

# #Holy Spells
# from .holy.heal import spell as heal

# #Acrane Spells
# from .arcane.rf_reg import spell as rf_reg
# from .arcane.svm_classifier import spell as svm_classifier
# from .arcane.umap_grim import spell as umap_grim
# from .arcane.fasttext_grim import spell as fasttext_grim
# from .arcane.spacy_ents_rels import spell as spacy_ents_rels
# from .arcane.image_classifier import spell as image_classifier


# #Water Spells
# from .water.highlight import spell as highlight

# #Nature Spells
# from .nature.histogram import spell as histogram
# from .nature.heatmap import spell as heatmap
# from .nature.scatter_plot import spell as scatter_plot
# from .nature.bar_chart import spell as bar_chart
# from .nature.line_chart import spell as line_chart
# from .nature.area_chart import spell as area_chart
# from .nature.stacked_bar import spell as stacked_bar
# from .nature.pair_plot import spell as pair_plot
# from .nature.three_d_plot import spell as three_d_plot


# #Air spells
# from .air.plot_map import spell as plot_map
# from .air.choropleth_map import spell as choropleth_map
# from .air.country_map import spell as country_map

# #Time spells
# from .time.time_bar_chart import spell as time_bar_chart
# from .time.time_line_chart import spell as time_line_chart
# from .time.animate_bubble import spell as animate_bubble

# REGISTERED_SPELLS = dict(
#     heal=heal,
#     rf_reg=rf_reg,
#     histogram = histogram,
#     heatmap = heatmap,
#     bar_chart = bar_chart,
#     scatter_plot = scatter_plot,
#     line_chart=line_chart,
#     area_chart=area_chart,
#     stacked_bar = stacked_bar,
#     svm_classifier= svm_classifier,
#     plot_map = plot_map,
#     time_bar_chart = time_bar_chart,
#     time_line_chart = time_line_chart,
#     animate_bubble = animate_bubble,
#     three_d_plot = three_d_plot,
#     pair_plot = pair_plot,
#     umap_grim = umap_grim,
#     fasttext_grim = fasttext_grim,
#     highlight = highlight,
#     choropleth_map = choropleth_map,
#     country_map = country_map,
#     spacy_ents_rels = spacy_ents_rels,
#     image_classifier= image_classifier
# )
