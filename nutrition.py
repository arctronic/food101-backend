import requests

url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

Headers = {
  "x-app-id":"8e1d67c8",
  "x-app-key": "02954c81e31ca277e7398414151b585c"
}

def get_nutrition(recipe):
  data = {
    "query": recipe
  }
  res = requests.post(url,headers=Headers, json=data)
  res = res.json()
  nut = {}
  if res["foods"]:
    details = res["foods"][0]
    nut["serving"] = str(details["serving_weight_grams"])+"g"
    nut["calories"] = str(details["nf_calories"])+"cal"
    nut["fat"] = str(details["nf_total_fat"])+"g"
    nut["cholesterol"] = str(details["nf_cholesterol"])+"g"
    nut["carbohydrate"] = str(details["nf_total_carbohydrate"])+"g"
    return nut
  return None