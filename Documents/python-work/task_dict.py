def my_code(dictionary, t_count=0):
	for key,value in dictionary.items():
		print("\t" * t_count + key+":")
		if isinstance(value,str):
			print("\t" * (t_count+1) + value)
		elif isinstance(value,dict):
			my_code(value,t_count+1)



my_code({'first': 'first_value','second': 'second_value'})
my_code({'1': {'child': '1/child/value'},'2': '2/value'})

