def main():
	f=open('./check/output.json')
	data = json.loads(f)
	max = 0
	list = []
	for it in data['match_percents']:
		if (it>=max):
			list.append(it)
	f.close()

if __name__ == '__main__':
	main()