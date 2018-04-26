# django_upload

запуск

* `pip3 install -r requirements.txt`
* `python3 manage.py makemigrations`
* `python3 manage.py migrate`
* `python3 manage.py createsuperuser`
* `python3 manage.py runserver <ip:port>`
* `celery worker -A django_upload --loglevel=debug --concurrency=1`

* `можно использовать мой адрес для теста <ip:port>=http://176.56.50.175:7777`
* `токены получать через админку, если использовать мой сервер, то токен <token> = fa875452fd22daad687c77df67e59f5ee4d25bc7`

запросы 

POST http://<ip:port>/image/upload/

* получение пикчи через интернал сервис. С указанием разрешений.
`
curl -X POST \
  http://<ip:port>/image/upload/ \
  -H 'authorization: Token 		<token>' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: d689c890-c12a-be48-b4e6-f3ed802933cc' \
  -F 'resolution=[
  {
    "width": 120,
    "height":888,
    "format_required":"png",
    "quality":1 }
]' \
  -F original=https://pp.userapi.com/c831208/v831208858/e3166/eSVk50OZCb0.jpg
`

* получение пикчи через форму. С указанием разрешений.

`
curl -X POST \
  http://<ip:port>/image/upload/ \
  -H 'authorization: Token 		<token>' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -H 'postman-token: f07531bc-8912-d2e2-6964-5f0de37aeddd' \
  -F 'resolution=[
  {
    "width": 120,
    "height":888,
    "format_required":"png",
    "quality":1 }
]' \
  -F original=@road_PNG46.png
`

* удаление пикчи

DELETE|GET http://<ip:port>/image/*.jpeg/

