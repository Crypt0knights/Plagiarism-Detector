import json

def main():
<<<<<<< HEAD
	f=open('./output.json')
=======
	f=open('./check/output.json')
>>>>>>> f55634ccf044a03725dd8c5708020d1da920f2ae
	data = json.load(f)
	urls={}
	final= {}

	for i in range(len(data)):
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