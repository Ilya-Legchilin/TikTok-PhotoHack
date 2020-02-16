import pandas as pd
import numpy as np
import bcolz
import pickle
import random
import os

class word2kek():
	def __init__(self):
		ROOT_DIR = os.path.dirname(os.path.abspath('tik-tok'))	
		CONFIG_PATH = os.path.join(ROOT_DIR, '6B.50.dat')

		words = []
		idx = 0
		word2idx = {}
		vectors = bcolz.carray(np.zeros(1), rootdir=CONFIG_PATH, mode='w')

		with open(os.path.join(ROOT_DIR, 'glove.6B.50d.txt'), 'rb') as f:
			for l in f:
				line = l.decode().split()
				word = line[0]
				words.append(word)
				word2idx[word] = idx
				idx += 1
				vect = np.array(line[1:]).astype(np.float)
				vectors.append(vect)

		vectors = bcolz.carray(vectors[1:].reshape((400000, 50)), rootdir=CONFIG_PATH, mode='w')
		vectors.flush()
		pickle.dump(words, open(os.path.join(ROOT_DIR, '6B.50_words.pkl'), 'wb'))
		pickle.dump(word2idx, open(os.path.join(ROOT_DIR, '6B.50_idx.pkl'), 'wb'))

		vectors = bcolz.open(os.path.join(ROOT_DIR, '6B.50.dat'))[:]
		words = pickle.load(open(os.path.join(ROOT_DIR, '6B.50_words.pkl'), 'rb'))
		word2idx = pickle.load(open(os.path.join(ROOT_DIR, '6B.50_idx.pkl'), 'rb'))

		self.glove = {w: vectors[word2idx[w]] for w in words}
	
		patterns_csv = pd.read_csv(os.path.join(ROOT_DIR, 'new_patterns.csv'), header=1)[['Pattern name', 'ID pattern']]
		patterns_csv = patterns_csv.dropna()
		patterns_np = patterns_csv.to_numpy()

		index2patterns = {i: w[0].lower() for i, w in enumerate(patterns_np)}
		self.index2ID = {i: w[1] for i, w in enumerate(patterns_np)}

		self.patterns_vec = np.zeros((len(patterns_csv), 50))
		for i in index2patterns:
			if type(self.glove.get(index2patterns[i], None)) == np.ndarray:
				self.patterns_vec[i, :] = self.glove.get(index2patterns[i], None)
	
	def get_id(self, word):
		if type(self.glove.get(word)) == np.ndarray:
			res = np.sum((self.patterns_vec - self.glove[word])**2, axis=-1)
			res = np.where(res == np.amin(res))[0]
			res = random.choice(res)
			return self.index2ID.get(res, 0)
		else:
			return 0

f = word2kek()

try:
    while True:
        print(f.get_id(input()))
except KeyboardInterrupt:
    print('interrupted!')



