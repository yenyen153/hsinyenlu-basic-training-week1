## 專案開發訓練
本次專案開發訓練，目的在於使用mariaDB內的資料，應用於FastAPI中</br>
整體專案分成三個部分進行</br>
- Part 1 爬蟲、Pydantic、Sqlalchemy、Database</br>
著重在講解mariaDB內的資料表設計，以及爬蟲任務細節說明</br>
</br>
- Part 2 FastAPI-get、post、put、delete</br>
本次使用FastAPI進行Restful API風格的實踐，使用到基本的get、post、put、delete對資料進行尋找、新增、修改、刪除</br>
</br>
- Part 3 頁面渲染</br>
因應訓練題目要求，以Jinja2Templates，提供更符合使用者應用之頁面

***
### Part1 爬蟲、Pydantic、Sqlalchemy、Database

#### 爬蟲
- 本次爬蟲目標：ptt
- 爬蟲版面：NBA, Baseball, mobilecomm, c_chat, lifeismoney, home-sale, stock
- 爬蟲任務：以celery完成每一小時定時爬蟲，以更新文章／爬取過去一年內資料
- 爬取內容：版面(board_name)、文章標題(title)、連結(link)、發文日期(date)、作者ptt id(author_ptt_id)、作者暱稱(author_nickname)、內文(content)

#### Pydantic
- 利用Pydantic驗證爬取後的資料，確保格式正確
- board_name需為字串(str)、title(str)、link(HttpUrl)、date(datetime)、author_ptt_id(str)、author_nickname(str)、content(str)

#### Sqlalchemy
- 以Sqlalchemy進行ORM操作資料庫，免去直接使用SQL語言

#### Databases
- 採用MariaDB關聯式資料表(table)
- 三個資料表，如下
</br>
**ptt_posts**：存放內建id、board_id(foreign key)、author_id(foreign key)、title(文章標題) 、link(連結)、date(發文日期)、content(內容)</br>
**board**：存放內建id、board(版面)、url(版面連結)</br>
**author**：存放內建id、author_ptt_id(作者ptt id)、author_nickname(作者暱稱)</br>
_ptt_posts內的board_id與board為關聯表格、author_id與author為關聯表格_

***
### Part2 FastAPI
訓練使用三種方式接受外部傳遞的變數</br>
path_parameter、query_parameter、request body</br>
path_parameter使用{}在路徑中設定一個參數，回傳該參數的值</br>
query_parameter接收不同變數並進行處理</br>
request_body使用者(Client)傳到API的資料，本次訓練以Pydantic去驗證使用者回傳的資料型態

#### get
- _**/posts/{post_id}**_  post_id表示ptt_post中的內建id，透過使用者指定post_id(必須是數字），回傳該位置的值
- _**/posts**_ 使用者透過不同的query，得到文章，並透過limit指定回傳文章的數量，offset選擇跳過的文章數量
- _**/statistics**_ 使用者透過不同的query，得到文章總數量
#### post
- _**/api/posts**_ 用於創建新文章，透過規定好的格式傳遞
#### put
- _**/api/posts/{post_id}**_ 用於更新文章，但必須是已存在的貼文，以post_id驗證貼文是否已存在
#### delete
- _**/delete/{post_id}**_ 透過post_id刪除文章

***
### Part3 頁面渲染
- 使用Jinja2Templates進行網頁渲染，提供更方便的使用介面