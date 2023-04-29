import requests
import json
import logging

_format = f"%(asctime)s [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s - %(pathname)s - %(msecs)d"

file = 'data/chef_helper.log'


file_handler = logging.FileHandler(file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(_format))


def get_logger(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
	return logger

logger = get_logger(__name__)
def get_reciept_by_name(name: str) -> list[dict]:

	url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
	querystring = {"query": name, "instructionsRequired": "true"}
	headers = {
		"content-type": "application/octet-stream",
		"X-RapidAPI-Key": "2e92981949mshe241e8b3014805cp11d7f5jsn5a51289967e8",
		"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	results = response.json()
	results = results.get('results')
	with open(f'reciept_{name}.json', 'w') as file:
		json.dump(results, file, indent=4)
	# print(results)
	return results

def get_reciept_via_id(meal_id: int) -> tuple[str, str]:

	url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{meal_id}/information"

	headers = {
		"content-type": "application/octet-stream",
		"X-RapidAPI-Key": "2e92981949mshe241e8b3014805cp11d7f5jsn5a51289967e8",
		"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers)

	result = response.json()
	title = result.get('title')
	instructions = result.get('instructions')

	return title, instructions


def search_receapt(user_input) -> str:
	# user_input = input('Enter the meal: ')
	results = get_reciept_by_name(user_input)
	meals_variation = dict()
	option = 1
	for item in results:
		meals_variation[option] = (item.get('id'))
		print(f'Option {option} (-_-)-> {item.get("title")}\n')
		option += 1

	new_input = int(input('Choose option: '))
	target_id = meals_variation[new_input]
	title, instruction = get_reciept_via_id(target_id)
	# logger.info(f'Your meal is: {title}\n')
	# logger.warning(f'Your meal is: {title}\n The coocking: {instruction}')
	return f'Your meal is: {title}\n The coocking: {instruction}'


if __name__=='__main__':
	# get_reciept_by_name('pizza')
	# print(get_reciept_via_id(2))
	# logger.debug('Start program!')
	print(search_receapt())


