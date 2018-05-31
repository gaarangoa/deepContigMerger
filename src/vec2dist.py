import h5py
import faiss
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from sklearn import manifold

f5 = h5py.File('vectors.h5', 'r')

data = f5['y_n']

print('computing ...')
x = manifold.TSNE(n_components=2).fit_transform(data)

print('plotting ...')
labels = {i.split('|')[0]: 1 for i in f5['index']}
cmap = plt.cm.get_cmap("hsv", len(labels))
labels = { i:cmap(ix) for ix,i in enumerate(labels) }

# labels = {
#     'CP009746': (0.0, 0.0, 0.0, 1.0),
#     'CP017022': (1.0, 0.0, 0.09375, 1.0),
#     'CP002643': (0.0, 0.07382819882819882, 1.0, 1.0),
#     'CP007803': (0.5234360234360234, 0.50, 0.50, 1.0),
#     'FQ312044': (0.0, 1.0, 0.21484500507147306, 1.0),
#     'CP017023': (1.0, 0.0, 0.09375, 1.0),
#     'FQ312039': (0.0, 1.0, 0.21484500507147306, 1.0),
#     'CP017021': (1.0, 0.0, 0.09375, 1.0),
#     'CP017020': (1.0, 0.0, 0.09375, 1.0)
# }

patch = [mpatches.Patch(color = labels[i], label = i) for i in labels]
plt.legend(handles = patch)
plt.scatter([i[0] for i in x], [i[1] for i in x], c=[labels[i.split('|')[0]] for i in f5['index']])
plt.show()

from sklearn.cluster import AgglomerativeClustering
clustering = AgglomerativeClustering(linkage='ward', n_clusters=10).fit(data)
