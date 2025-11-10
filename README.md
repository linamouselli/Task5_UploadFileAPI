##Uploads Files API (Django DRF Task)
This task for upload files via API and I used the below:
1- MySQL server database
2- Session Authentication
3- Rate Limiting is enabled

username for admin superuser and session login authentication are:
username = admin

The steps for run the project:
git clone <REPO_URL>
cd session15Project
python -m venv .venv
#Activate virtual environment
.venv\Scripts\activate

#for download required packages
pip install -r requirements.txt
python manage.py migrate

#create superuser
python manage.py createsuperuser

python manage.py runserver

#I tested using Nginx, but i depends on the normal way 'python manage.py runserver'
#for Nginx we use the command: waitress-serve --listen=127.0.0.1:8000 session15.wsgi:application 

curl examples:
According to that I am using Windows, the curl will be different from Linux

Example1 for Windows cmd - upload correct file:
curl -b "sessionid=<SESSION_ID>; csrftoken=<CSRF_TOKEN>" -X POST http://127.0.0.1:8000/api/uploads/ -H "X-CSRFToken: <CSRF_TOKEN>" -F "file=@E:\2024\Other files\Icon.png"

Example1 for Linux - upload correct file:
curl -b "sessionid=<SESSION_ID>; csrftoken=<CSRF_TOKEN>" \
     -X POST http://127.0.0.1:8000/api/uploads/ \
     -H "X-CSRFToken: <CSRF_TOKEN>" \
     -F "file=@/E:/2024/Other files/Icon.png"

Example2 for Windows cmd - upload unsupported file extension:
curl -b "sessionid=<SESSION_ID>; csrftoken=<CSRF_TOKEN>" -X POST http://127.0.0.1:8000/api/uploads/ -H "X-CSRFToken: <CSRF_TOKEN>" -F "file=@E:\2024\Other files\maleware.exe"
curl -b "sessionid=<SESSION_ID> csrftoken=<CSRF_TOKEN>" -X POST http://127.0.0.1:8000/api/uploads/ -H "X-CSRFToken: <CSRF_TOKEN>" -F "file=@E:\2024\Other files\Icon.gif"

Example3 for Windows cmd - List of files:
curl -b "sessionid=<SESSION_ID>" "http://127.0.0.1:8000/api/uploads/?page=1"

Example4 for Windows cmd - Details of a file:
curl -b "sessionid=<SESSION_ID>" "http://127.0.0.1:8000/api/uploads/11/"**

#I get the session id and csrftoken values from browser while testing. However, i hide them from the README.md file