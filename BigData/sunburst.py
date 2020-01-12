import plotly.graph_objects as go
from Algorithms import dictionary_dimension_conversion
import json

Graph8 = "social_media_comments_by_product_line.json"
with open (Graph8, "r") as file:
    Graph8_Data = json.load(file)

algo = dictionary_dimension_conversion(Graph8_Data)
dictionary_1 = algo.dict_conversion()


total = sum(list(dictionary_1.values()))

labels2 = ["Total"]
parents2 = [""]
values2 = [total]
for key, value in dictionary_1.items():
    labels2.append(key)
    parents2.append("Total")
    values2.append(value)

    label_extension = list(Graph8_Data.get(key).keys())

    product_line = key + " "
    product_line_list = ((product_line * len(label_extension)).split(" "))
    product_line_list.pop()
    parents_extension = product_line_list

    values_extension = list(Graph8_Data.get(key).values())

    labels2.extend(label_extension)
    parents2.extend(parents_extension)
    values2.extend(values_extension)



fig = go.Figure(
    go.Sunburst(
        labels=labels2,
        parents=parents2,
        values=values2,
        branchvalues="total",
        maxdepth=2
    )
)

fig.show()