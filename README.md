Mova-se!
========
Website / Blog developed with Django


Installation / Usage
--------------------

1. Clone the project

    ``` sh
    $ git clone https://github.com/laborautonomo/movase.git
    $ cd movase
    ``` 

2. Create and active [vitualenv](http://pypi.python.org/pypi/virtualenv)

    ``` sh
    $ virtualenv venv
    $ source venv/bin/activate
    ``` 

3. Download and install requirements with [pip](http://pypi.python.org/pypi/pip)

    ``` sh
    $ pip install -r requirements.txt
    ```

4. Configure the project in `movase/settings.py` file

5. Syncronize database with `$ python manage.py syncdb`

6. Collect static files with `$ python manage.py collectstatic`

7. Finally, run `$ python manage.py runserver`

Internet Archive importing contents
-----------------------------------
The `ia_client_api` APP import the archive.org contents to CMS APP using Bookmarks list as reference.

#### Using the IA_CLIENT_API
1. Set the `IA_BOOKMARKS` parameter of `movase/settings.py`
2. Call the command to import content: `$ python manage.py ia_import`


References
----------

* [Django documentation](https://docs.djangoproject.com/en/1.6/)
* [aprendendo-django](https://github.com/marinho/aprendendo-django)