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

patch = [mpatches.Patch(color = labels[i], label = i) for i in labels]
plt.legend(handles = patch)
plt.scatter([i[0] for i in x], [i[1] for i in x], c=[labels[i.split('|')[0]] for i in f5['index']])
plt.show()

from sklearn.cluster import AgglomerativeClustering
clustering = AgglomerativeClustering(linkage='ward', n_clusters=10).fit(data)
