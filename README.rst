==========
 bucketapp
==========

.. image:: https://travis-ci.org/clemwek/bucketapp.svg?branch=master
    :target: https://travis-ci.org/clemwek/bucketapp

.. image:: https://coveralls.io/repos/github/clemwek/bucketapp/badge.svg?branch=master
    :target: https://coveralls.io/github/clemwek/bucketapp?branch=master



What would you like to do in the next few years? Climb a mountain? Learn to ride a bike? :) It’s important to  keep track of what you have already done and what you are yet to achieve. Register and start tracking.

To access the live app click here_.

.. _here: https://lit-lake-37731.herokuapp.com/

Installing
==========


Make sure you have python installed in your system if not visit https://www.python.org/downloads/ and get a copy for your system

Clone the project 
 ``git clone https://github.com/clemwek/bucketapp.git <foldername>``
 

Change Directory into the project folder
 ``cd <foldername>``

Create a virtual environment with Python
    ``$ virtualenv -p python3 <yourenvname>``

Activate the virtual environment
    ``$ source <yourenvname>/bin/activate``
    

Install the application's dependencies from requirements.txt to the virtual environment
    ``$ pip install -r requirements.txt``
    

Run the app on port 5000
    ``python bucketlistapp/bucketlistapp.py``
    
Access the page in the browser 
    ``localhost:5000``



Testing
=======

To test the app run the following command
    ``nosetests bucketlistapp/tests``
    
    
