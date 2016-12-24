import requests
from lxml import html

import numpy as np
import matplotlib.pyplot as plt

# Blog urls
urls = """
Add your blogger urls here
""".strip().split("\n")

names = []
for url in urls:
    print "Loading", url + "..."
    xpath = "//div[@class='widget-content']/div/table/tbody/tr/td[2]/text()"
    text = requests.get(url).text
    root = html.fromstring(text)
    result = root.xpath(xpath)
    
    names.extend([x.translate(None, ",.-") for x in result \
        if len(x.strip()) != 0])


def analyse(cut_names):
    data = {}
    unique_names = set(cut_names)
    for name in unique_names:
        data[cut_names.count(name)] = data.get(cut_names.count(name), []) + \
                [name]

        cut_names = [x for x in cut_names if x != name]

    return data

cut_names = []
for name in names:
    cut_names.extend(name.split())
    
d = analyse(cut_names)

x_axis = []
for key in sorted(d.keys()):
    x_axis.extend(d[key])

y_axis = []
for key in sorted(d.keys()):
    y_axis.extend([key] * len(d[key]))

y_axis.reverse()
x_axis.reverse()

fig = plt.figure()

axes = plt.subplot(111)
axes.bar(np.arange(len(y_axis)), y_axis, width=1.0)

axes.set_yticks(np.arange(max(y_axis)))
axes.set_xticks(np.arange(len(x_axis)) + 0.15)
axes.set_xticklabels(x_axis, rotation=90, ha="center")

plt.xlim([0, 80])
plt.show()
