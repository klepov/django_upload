# django_upload

запуск

* `pip3 install -r requirements.txt`
* `python3 manage.py makemigrations`
* `python3 manage.py migrate`
* `python3 manage.py createsuperuser`

запросы 

POST http://176.56.50.175:7777/image/upload/

* получение пикчи через интернал сервис. С указанием разрешений.
`
curl -X POST \
  http://176.56.50.175:7777/image/upload/ \
  -H 'authorization: Token 		8be127eb55776220316b93f503b9c48e7073beb5' \
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
  http://176.56.50.175:7777/image/upload/ \
  -H 'authorization: Token 		8be127eb55776220316b93f503b9c48e7073beb5' \
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

DELETE|GET http://176.56.50.175:7777/image/*.jpeg/

