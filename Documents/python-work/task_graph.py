def my_code(adjacency_list, vertex, vertexes = None):
	if vertexes is None:
		print("\n")
		vertexes = []
	if vertex not in vertexes:
		print(vertex)
		vertexes.append(vertex)
		for key,value in adjacency_list.items():
			if vertex == key:
				adjacency_copy= adjacency_list.copy()
				del adjacency_copy[vertex]
				for v in value:
					my_code(adjacency_copy,v, vertexes)


data = {1: [2, 3],2: [4]}
my_code(data, 1)
data = {1: [2, 3],2: [3, 4],4: [1]}
my_code(data, 1)
