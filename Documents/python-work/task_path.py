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
		# return list of paths from specification belongs to class path
		class_obj = class_path[class_path.rfind("/")+1:]#name of class from path
		specvalueslist = []
		if class_obj in specification:
			for specvalue in specification[class_obj]:
				new_path_string = class_path + "/" + specvalue
				specvalueslist.append(new_path_string)
		return specvalueslist

	def get_potential(self, class_path, specification):
		result = []
		queue = ["/" + class_path]
		while queue:
			result.extend(queue)
			queue = self.get_chain_list(queue, specification)
		return result

	def get_chain_list(self, queue, specification):
		queue = list(chain.from_iterable(
			self.iter_paths(item, specification)
			for item in queue
		))
		return queue



	def get_applicable(self, class_path, specification):
		queue_alg = [["/" + class_path]]
		result = {}
		while queue_alg:
			for queue_alg_inner in queue_alg:
				while queue_alg_inner:
					queue_sum = []
					ident_path = ''
					temp_list = [] #list for paths with common part
					queue_alg_inner = self.get_chain_list(queue_alg_inner, specification)
					for item in queue_alg_inner:
						queue_sum.append(item.split())
						ident_path_current = item[:queue_alg_inner[0].rfind("/")]#get parent path
						if ident_path_current==ident_path:		
							# items have a common parent path
							temp_list.append(item)
							result[ident_path_current] = temp_list
						else:
							# items have different parent paths
							ident_path = ident_path_current
							temp_list.append(item)
							result[ident_path_current] = item.split()
				queue_alg = queue_sum
		return result

	def my_method(self, source_object):
		result = {}
		alg_dict = {}
		potencial_list = []
		class_name = source_object.__name__
		result['Algorithm'] = alg_dict
		for algorithm in self.algorithm_list:
			alg_step_dict= {}
			spec = {}
			# get specification
			for key,value in getattr(algorithm, 'SPECIFICATION').items():
				values_list = []
				for v in value:
					values_list.append(v.__name__)
					spec[key.__name__] = values_list

			if class_name in spec:
				# Potencial paths
				potencial_list.extend(self.get_potential(class_name, spec))
				# Algorithm paths
				alg_step_dict = self.get_applicable(class_name, spec)

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
	Lemon: [Orange, Apple],
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
