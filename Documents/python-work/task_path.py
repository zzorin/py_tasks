from itertools import chain
import json

class Component:
	def __init__(self, *algorithm_list):
		self.algorithm_list = algorithm_list
	def __call__(self, source_object):
		result = []
		queue = [source_object]
		# print(queue)
		while queue:
			# print(result)
			result.extend(queue)
			# print(queue)
			queue = list(chain.from_iterable(
				algorithm(item)
				for item in queue
				for algorithm in self.algorithm_list
			))
			print("queue")
			print(queue)
		return result

	def iter_alg(self, alg_step_dict, path_string, class_obj, specification):
		if class_obj in specification:
			specvalueslist = []
			for specvalue in specification[class_obj]:
				new_path_string = path_string + '/' + specvalue
				specvalueslist.append(new_path_string)
				self.iter_alg(alg_step_dict, new_path_string, specvalue, specification)
			alg_step_dict[path_string] = specvalueslist	
		return alg_step_dict

	def iter_potencial(self, path_string, class_obj, specification):
		specvalueslist = []
		if class_obj in specification:
			for specvalue in specification[class_obj]:
				new_path_string = path_string + '/' + specvalue
				specvalueslist.append(new_path_string)
				specvalueslist.extend(self.iter_potencial(new_path_string, specvalue, specification))
		return specvalueslist

	def my_method(self, source_object):
		result = {}
		alg_dict = {}
		potencial_list = []
		result['Algorithm'] = alg_dict
		for algorithm in self.algorithm_list:
			alg_step_dict = {}
			alg_dict[algorithm.__class__.__name__] = alg_step_dict
			spec2 = {}
			spec = getattr(algorithm, 'SPECIFICATION')
			for key,value in spec.items():
				values_list = []
				for v in value:
					values_list.append(v.__name__)
					spec2[key.__name__] = values_list
			if source_object.__name__ in spec2:
				potencial_list.append(source_object.__name__)
				potencial_list.extend(self.iter_potencial("/" + source_object.__name__, str(source_object.__name__), spec2))
			alg_dict[algorithm.__class__.__name__] = self.iter_alg({}, "/" + source_object.__name__, str(source_object.__name__), spec2)
		result['Potential'] = potencial_list
		return result


class Apple:
	pass

class Orange:
	def __init__(self, number):
		self.number = number

class Lemon:
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
print(component(Lemon()))

# print(json.dumps(component.my_method(Lemon), indent=4))
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
