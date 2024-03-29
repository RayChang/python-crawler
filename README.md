# 爬取 YAHOO 汽車

爬取 YAHOO 汽車上有的車款資料

## 程式說明

第一次嘗試使用 selenium 開啟瀏覽器，想抓取 Select DOM 上的 Options 的內容

結果發現當 `<select id="car_make_id" />` 變更時，隔壁的 `<select id="car_model_id" />` 的 DOM 會重新繪製，導致我在 selenium 裡會噴錯

也因為這樣所以發現當切換 select option 的時候前端的畫面會去呼叫 API

所以我就改由先抓取 `<select id="car_make_id" />` 的所有 option value 後透過迴圈去打 API 結果拿回來的資料更多更齊全

但過程中有發現打 API 時 header 裡要帶入 `At-Authorization` 才不會造成 401

然後會打兩支 API 一個是透過 `car_make_id` 去拿 Car Model 再透過 `car_model_id` 去拿型號

最終會輸出一份 cars_data 的 json

但因為資料太大了，所以在使用 `car_model_id` 打 API 的時候只打第一項的內容
