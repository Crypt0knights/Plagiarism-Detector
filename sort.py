import json

def main():

	f=open('./output.json')
	data = json.load(f)
	urls={}
	final= {}
	for i in range(len(data)):
		if data[i]['match_url'] == None:
			pass
		else:
			urls[data[i]['match_percents']]=data[i]['match_url']

	
	sort_percent = sorted(urls, reverse = True)[:5]
	print(sort_percent)

	for key in sort_percent:
		final[key] = urls[key]

	with open('url_percent.json','w') as url_json_file:
		json.dump(final, url_json_file,sort_keys=True,indent=5)

	f.close()


if __name__ == '__main__':
	main()