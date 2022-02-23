## The <span style="color:red">*Issue Manager*</span> Project


### Installation
```sh
	cd project_dir
	pip install -r requirements.txt
	python manage.py createsuperuser
	python manage.py check
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
```
Now, you can view the application with this url [http://localhost:8000/](http://localhost:8000/)


### Rest urls
* To view all tasks:  [http://localhost:8000/task/api/list/](http://localhost:8000/task/api/list/)
* To create a new task:  [http://localhost:8000/task/api/create/](http://localhost:8000/task/api/create/)
* To retrieve task:  [http://localhost:8000/task/api/retrieve/<int:pk>](http://localhost:8000/task/api/retrieve/<int:pk>)
* To update task:  [http://localhost:8000/task/api/update/<int:pk>](http://localhost:8000/task/api/update/<int:pk>/)
* To delete a task:  [http://localhost:8000/task/api/delete/<int:pk>](http://localhost:8000/task/api/delete/<int:pk>/)

### Samples with curl on Localhost: 
* **task - list**
    ```commandline
    curl  --location --request GET 'http://localhost:8000/task/api/list/'
    ```

* **task - create** 
    ```commandline
    curl --user 'guest:123456'  --header "Content-Type: application/json" --location --request POST 'http://localhost:8000/task/api/create/' \
    --data-raw '{
        "title": "Create New page",
        "status": 1,
        "description": "Create New Welcome Page!"
    }'
    ```


* **task - retrieve** 
    ```commandline
    curl --user 'guest:123456' --location --request GET 'http://localhost:8000/task/api/retrieve/52'
    ```

* **task - update**

    ```commandline
    curl --user 'guest:123456'  --header "Content-Type: application/json" --location --request PUT 'http://localhost:8000/task/api/update/53/' \
    --data-raw '{"title": "Change font", "status": 1, "description": "Change font to awesome"}'
    ```

* **task - delete**
    ```commandline
    curl --user 'guest:123456'  --location --request DELETE 'http://localhost:8000/task/api/delete/31/'
    ```



### Built With

* [Python](https://python.org)
* [Django](https://djangoproject.com)
* [Bootstrap](https://getbootstrap.com)

## Contact
kanz84 -  kanz1384@gmail.com
