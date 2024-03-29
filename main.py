import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json

# Yahoo API 的 AT-Authorization 有可能會過期，請自行更新
auth: str = "e1eba75272ae3ea4fa9e80459949feda4e63133a"

model_fetch_path: str = "model/list/make"
trim_fetch_path: str = "trim/list/model"

# 獲取車款與型號列表
def fetch(id: str, path: str, target: str):
  url: str = f"https://autos.yahoo.com.tw/v1/autos/newcar/{path}/{id}?get_all=true"
  response = requests.get(url, headers={"At-Authorization": auth})
  print('response.status_code: ', response.status_code)
  if response.status_code == 200:
    data = response.json()
    return data.get('autos', {}).get('result', [])[0].get(target, [])
  return []


def main():
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service)
  driver.get("https://autos.yahoo.com.tw/cars-compare")

  WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "car_make_id"))
  )
  select_element = Select(driver.find_element(By.ID, "car_make_id"))
  cars_data = {}

  for option in select_element.options[1:]:  # 跳過第一個提示性選項
    make_id = option.get_attribute('value')
    print('make_id: ', make_id)
    if make_id:  # 確保 make_id 不為空
      make_text = option.text.strip().replace(' ', '_')
      model_list = fetch(make_id, model_fetch_path, 'modellist')
      cars_data[make_text] = model_list
      print(f"Fetched {make_text}: {len(model_list)} models.")
      time.sleep(2)  # 每次請求之間暫停 2 秒，避免被 Yahoo 封鎖
  
  key_list = list(cars_data.keys())
  for key in key_list[:1]: # 只取第一個 key 做測試，全跑完可能要等很久
    for model in cars_data[key]:
      trim_list = fetch(model.get('model_id'), trim_fetch_path, 'trimlist')
      model['trim'] = trim_list
      print(f"Fetched {key} {model.get('model_name')}: {len(trim_list)} trims.")
      # 不減速的話會被 Yahoo 封鎖
      time.sleep(5)

  # Convert cars_data to JSON
  json_data = json.dumps(cars_data)

  # Write JSON data to a file
  with open('./cars_data.json', 'w', encoding='utf-8') as file:
    file.write(json_data)
  driver.quit()

if __name__ == "__main__":
  main()
