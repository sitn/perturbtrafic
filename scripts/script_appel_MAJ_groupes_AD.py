import requests
url_ws = "http://localhost/perturbtrafic_api/perturbtrafic/api/mise_a_jours_groupes_ad"

try:
	r = requests.get(url_ws)
	
	if(r.status_code != 200):
		print("An error occured when calling url: '" + url_ws + "'")
	else:
		print(r.content)

except Exception as e:
	print(str(e))