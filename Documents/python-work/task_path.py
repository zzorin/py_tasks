from itertools import chain
import json

class Component:
	def __init__(self, *algorithm_list):
		self.algorithm_list = algorithm_list
	def __call__(self, source_object):
		result = []
		queue = [source_object]
		while queue:
			result.extend(queue)
			queue = list(chain.from_iterable(
				algorithm(item)
				for item in queue
				for algorithm in self.algorithm_list
			))
		return result

	def iter_paths(self, class_path, specification):
		# print(class_path)
		class_obj = class_path[class_path.rfind("/")+1:]
		specvalueslist = []
		if class_obj in specification:
			for specvalue in specification[class_obj]:
				new_path_string = class_path + "/" + specvalue
				specvalueslist.append(new_path_string)
		return specvalueslist

	def my_method(self, source_object):
		result = {}
		alg_dict = {}
		potencial_list = []
		result['Algorithm'] = alg_dict
		for algorithm in self.algorithm_list:
			alg_step_dict= {}
			spec = {}
			for key,value in getattr(algorithm, 'SPECIFICATION').items():
				values_list = []
				for v in value:
					values_list.append(v.__name__)
					spec[key.__name__] = values_list
			if source_object.__name__ in spec:
				# Potential paths
				queue = ["/" + source_object.__name__]
				while queue:
					potencial_list.extend(queue)
					queue = list(chain.from_iterable(
						self.iter_paths(item, spec)
						for item in queue
					))
				# Algorithm paths
				queue_alg = [["/" + source_object.__name__]]
				
				while queue_alg:
					for queue_alg_inner in queue_alg:
						while queue_alg_inner:
							queue_sum = []
							queue_alg_inner = list(chain.from_iterable(
								self.iter_paths(inner_item, spec)
								for inner_item in queue_alg_inner
							))
							for item in queue_alg_inner:
								queue_sum.append(item.split())
							ident_path = ''
							temp_list = []
							for item in queue_alg_inner:
								ident_path_current = item[:queue_alg_inner[0].rfind("/")]
								if ident_path_current==ident_path:		
									temp_list.append(item)
									alg_step_dict[ident_path_current] = temp_list
								else:
									ident_path = ident_path_current
									temp_list.append(item)
									alg_step_dict[ident_path_current] = item.split()
						queue_alg = queue_sum


			alg_dict[algorithm.__class__.__name__] = alg_step_dict
		result['Potential'] = potencial_list
		return result


class Apple:
	pass

class Orange:
	def __init__(self, number):
		self.number = number

class Lemon:
	pass

class Lemon2:
	pass

class Lemon3:
	pass

class FirstAlgorithm:
	SPECIFICATION = {
	Orange: [Apple],
	Lemon: [Orange, Apple]
	}
	def __call__(self, source_object):
		if isinstance(source_object, Orange):
			return [
			Apple()
			for _ in range(source_object.number)
			]
		if isinstance(source_object, Lemon):
			return [Orange(3), Apple()]
		return []

class EmptyAlgorithm:
	SPECIFICATION = {}
	def __call__(self, source_object):
		return []

component = Component(FirstAlgorithm(), EmptyAlgorithm())

print(json.dumps(component.my_method(Lemon), indent=4))
# print(json.dumps( {'Potential': [
#  	'/Lemon',
# 	 '/Lemon/Orange',
# 	 '/Lemon/Apple',
# 	 '/Lemon/Orange/Apple'
# 	 ],
# 	 'Algorithm': {
# 	 'FirstAlgorithm': {
# 	 '/Lemon': [
# 	 '/Lemon/Orange',
# 	 '/Lemon/Apple'
# 	 ],
# 	 '/Lemon/Orange': [
# 	 '/Lemon/Orange/Apple'
# 	 ]
# 	 },
# 	 'EmptyAlgorithm': {}
# 	 }
# 	}, indent=4))
