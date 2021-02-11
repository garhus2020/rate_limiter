# Rate Limiter in Flask

Rate Limit is the maximum number of API requests which users can make per hour

To run the application you need to have **docker** installed on your computer.

After installing docker or if you have it already installed run the following commands:

Build docker image:

```docker image build -t flask-app .```

Now run the docker image:

```docker run -p 5001:5000 -d flask-app```

Now open [localhost:5001/date/](http://localhost:5001/date/) in your your browser.

It will output date at every request untill the limit is reached for the last hour  (with the heaaders : X-RateLimit-Limit , X-RateLimit-Remaining ). 

The limit and the period can be changed in config file **conf.ini**

