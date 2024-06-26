                         
<br/>
<div align="center">
<a href="https://github.com/Mahboob-A/algocode">
<img src="https://github.com/Mahboob-A/algocode/assets/109282492/90d1dbfb-5542-485d-a1f5-2e347248c07d" alt="Logo" width="700" height="400">
</a>
<h3 align="center">Algocode - The Leetcode for Hackers</h3>
<p align="center">
Algocode is a DSA practice platform just like Leetcode!
<br/>
<br/>
<a href="https://imehboob.medium.com/my-experience-building-a-leetcode-like-online-judge-and-how-you-can-build-one-7e05e031455d"  target="_blank" ><strong>Read the blog »</strong> </a>
<br/>
<br/>
<a href="https://github.com/Mahboob-A/algocode-auth">Algocode Auth Service .</a>  
<a href="https://github.com/Mahboob-A/code-manager">Code Manager Service .</a>
<a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a>
</p>
</div>

<h3 align="center">General Information</h3>

Algocode is an online data structure and algorithm practice backend built in microservices architecture. 


*Algocode currently has three services*: <a href="https://github.com/Mahboob-A/algocode-auth">Algocode Auth Service .</a> <a href="https://github.com/Mahboob-A/code-manager">Code Manager Service .</a> and <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a>
<br/> <br/>

`Code Manager Service` is responsible to interact with client side to handle `code submission requests` and manage `code execution` in the <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a>. 

To learn more about _Algocode and the architecture_, please `READ-THE-BLOG-URL` or visit <a href="https://github.com/Mahboob-A/algocode">Algocode</a> here. 


#### _NOTE_

**A. Rate Limit Alert**

> The API endpoint to submit solution to the Algocode platfrom (Implemented  using _Token Bucket Algorithm_ <a href="https://github.com/Mahboob-A/code-manager/blob/main/src/core_apps/code_submit/RateLimitMiddleware.py">Rate Limit Middleware </a>) is rate limited to `1 request per 20 seconds`. 
>> ```http 
>>     POST https://codemanager.algocode.site/api/v1/code/submit/
>> ``` 

**B. Documentation**

Please visit the <a href="https://cm-doc.algocode.site/doc/">documentation page</a>  for the detailed guide on Algocode Code Manager Service.

> However, all the APIs are referenced in the **_API Reference_** section below.

**C. Deployment**

> The service is deployed in AWS EC2 Ubuntu 22.04 server.

**D. About Algocode**

> This is Code Manager Service specific guideline.
>> **Please visit <a href="https://github.com/Mahboob-A/algocode">Algocode</a> to learn the mircroservices architecture of Algocode and more in-depth guideline how to submit a solution to Algocode platform.**



<br/> <br/><details>
<summary><h3 align="center">Production</h3></summary>

#### Production Stage Code Manager

The Algocode Code Manager Services uses the following services to serve the request during Production Stage.  

    a. Nginx as webserver.
    b. Nginx Proxy Manager to manage Nginx.
    c. Portainer to manage and monitor docker container in Code Manager Service. 
    d. Gunicorn as application server.
    e. RabbitMQ for asynchronous message processig.
    f. Django as backend. 
    g. Django Rest Framework for API. 
    h. PostgreSQL for Algocode questions/problems database.
    i. Redis for cache. 
    j. MongoDB to store code execution result.
    k. Docker to containerize the service. 

#### Deployment

The Code Manager Service is deployed in AWS EC2 Ubuntu 22.04 Server. 

<br/>
<br/>  

</details><details>
<summary><h3 align="center">Workflow - Code Manager </h3></summary>

#### Overview 

Code Manager Service acts as middleman between the clients and the <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a> to handle `code submission` and `code execution`. 

The client can not directly interact with the <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a> as it is a secure and isolated environment to actually `execute the user submitted code` in the Algocode platform. Code Manager acts as the connecting dots between the client and the RCE Engine service from `solution submission` to `result persistence` process.  


##### Workflow 

The user submits the solution of the problem they want to submit through the `code submission API`. The API processes the data and publishes the data in a`RabbitMQ instance`. The <a href="https://github.com/Mahboob-A/rcee/">RCE Engine Service</a> consumes the message and `executes the user submitted code` and `generates a result` comparing the `testcases` and the output of the `user submitted code`. 

Once a result is generated, the RCE Engine publishes the `code execution result` to a `unified result queue`, Code Manager Services listens to the `unified result queue`. 

Code Manger processes the message from the `unified result queue`, `caches it in Redis` and stores the result in `MongoDB` database for persistence.   


<br/>
<br/>  

</details>


<details>
<summary><h3 align="center">Watch In Action</h3></summary>


#### A. Long Video (Describes all the features and architecture)
- Watch from `16:30` for code execution begin and  `18:30` for code submission result. 

<a href="https://www.youtube.com/watch?v=TbiRWL-11Fo&t=990s" target="_blank">
  <img src="https://img.youtube.com/vi/TbiRWL-11Fo/0.jpg" alt="Watch the video">
</a>

#### B. Short Video (Only core features) 
- Watch from `09:30` for code execution begin and  `11:30` for code submission result. 

<a href="https://www.youtube.com/watch?v=EgtAEjH53BA&t=571s" target="_blank">
  <img src="https://img.youtube.com/vi/EgtAEjH53BA/0.jpg" alt="Watch the video">
</a>

<br/>
<br/>  
</details>


<details>
<summary><h3 align="center">API Reference - Code Submission and Submission Result</h3></summary>

#### Problem Lists 

To learn about the Problems in Algocode without calling API, Please visit <a href="https://algocode.notion.site/Algocode-Problem-Lists-c9868c2fb29f43719c638e2e7d337f9a?pvs=4">Algocode Problem Lists</a> to get all the available problems. 

> I have used notion page to host the available problems in Algocode as I am focusing on advanced backend engineering, and  as there is no client app for Algocode at the time I am writing this Readme. 
> 
> If you want to contribute to build a client app for the Algocode, pelase do not hesitate to email here: 
> [![Email Me](https://img.shields.io/badge/mahboob-black?style=flat&logo=gmail)](mailto:connect.mahboobalam@gmail.com?subject=Hello)
> 
> To learn more on Algocode and the microservices architecture of Algocode; and more detailed guide on how to submit a solution, please <a href="https://github.com/Mahboob-A/algocode">visit algocode</a> here. 

<br/>

##### Code Submission API

```http
    POST https://codemanager.algocode.site/api/v1/code/submit/
```

| Parameter | Type     | Value/Description                |
| :-------- | :------- | :------------------------- |
| `problem_id`    | `string` | **Required**. The `problem_id` of the problem you are submitting the solution. |
| `lang` | `string` | **Required**. `cpp`. Currently `cpp` is supported. `java` RCE Engine is under development. |
| `code`    | `string` | **Required**. Your solution for the problem in `JSON` format.|

The `queue` is based on the `programming language` of the solution.  

<br/> 

##### Example Payload 

Here's an example payload for one of a problem in Algocode `Sqrt(X)`. The problem is same as this <a href="https://leetcode.com/problems/sqrtx/">Leetcode Problem.</a>

<br/> 

`Example Payload`

```
{
    "problem_id": "f17f511a-8c53-41d3-b750-7673d25835af", 
    "lang": "cpp", 
    "code": "#include <iostream>\n\nint mySqrt(int x) {\n    if (x == 0) return 0;\n    int left = 1, right = x, result = 0;\n    while (left <= right) {\n        
     int mid = left + (right - left) / 2;\n        if (mid <= x / mid) {\n            result = mid;\n            left = mid + 1;\n        } else {\n            right = mid - 1;\n        }\n    
    }\n    return result;\n}\n\nint main() {\n    int t;\n    std::cin >> t;\n    while (t--) {\n        int x;\n        std::cin >> x;\n        std::cout << mySqrt(x) << 
    std::endl;\n    }\n    return 0;\n}\n"
}
``` 
<br/>


##### Code Submission Result API

The second API of the Code Manager service is to `check the result of an code submission` to the Algocode platform.   

The API is a `Short Polling API`. It checks the data in `cache`, then in `MongoDB Database` and if the data could not be found, it `waits for 5 seconds` for the availability of the data.  
<br/>

```http
    GET  https://codemanager.algocode.site/api/v1/result/check/<submission_id>/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `submission_id`    | `string` | **Required**. The `submission_id` of your solution as per the `API Guideline - Code Submission in Algocode` section.|


<br/>
<br/>  

</details><details>
<summary><h3 align="center">API Reference - Problem List APIs</h3></summary>

#### All Problems in Algocode 

The API response is paginated with 10 results. 

```http
    POST https://codemanager.algocode.site/api/v1/problem/all/
```

#### Specific Problem in Algocode

Any specific problem using problem `id`. 

```http
    POST https://codemanager.algocode.site/api/v1/problem/<uudi:id>/
``` 
| Parameter |   Type     | Description  |
| :-------- | :------- | :------------------------- |
| `id`    | `string` | **Required**.  The `id` of the problem/question. |


#### Healthcheck 

```http
     GET  https://codemanager.algocode.site/api/v1/common/healthcheck/
```

Please visit <a href="https://cm-doc.algocode.site/doc/">the documentation page</a>  for more details.

<br/>
<br/>  

</details><details>
<summary><h3 align="center">Run Locally and Contribution</h3></summary>

#### Run Locally

Please `fork` and `clone` this <a href="https://github.com/Mahboob-A/code-manager/tree/development">development branch</a> of Algocode Code Manager Service, and follow along with the `envs-examples`. 

`cd` to `src` and create a `virtual environment`. Activate the virtual environment. 

Run `make docker-up` and the development setup will start running. Please install `make` in your host machine. 

If you use `Windows` Operating System, please run the  respective `docker commands` from the **`dev.yml`** docker compose file.

#### Contribution 

You are always welcome to contribute to the project. Please `open an issue` or `raise a PR` on the project.  

<br/>
<br/>  

</details>
<details>
  <summary><h3 align="center">Code Submission Result Examples</h3></summary>

<br/>

#### Some Code Submission Result Snapshots

<br/> 

##### A. AC Solution 

 ![dd8dbfe4-621b-49f1-b3a6-7ab2a892db87](https://github.com/Mahboob-A/algocode/assets/109282492/378d23ae-e059-47eb-866d-7c73d329b430) 
<br/>
<br/>

##### B. WA Solution 

  ![bedb4255-86c9-4417-b920-5976e6129cbb](https://github.com/Mahboob-A/algocode/assets/109282492/69bce2c1-5e16-4685-9069-23492068b55e)
<br/>
<br/>

##### C. Compilation Error

![1c5edd39-8ccd-4e23-a61d-66ae9564ca85](https://github.com/Mahboob-A/algocode/assets/109282492/9df40b17-b3f9-48d4-9662-3acdc1f594b8) 
<br/>
<br/>


##### D. Segmentation Fault 

![WhatsApp Image 2024-06-05 at 11 42 42 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/0a3e1d3f-bafb-41a4-8f30-29eb5a9133e5)
<br/>
<br/>


##### E. Memory Limit Exceed

![WhatsApp Image 2024-06-05 at 11 42 03 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/766f01f7-e97a-4aa7-858a-d7dddbf89b7d)
<br/>
<br/>


##### F. Time Limit Exceed 

![WhatsApp Image 2024-06-05 at 11 42 03 PM (1)](https://github.com/Mahboob-A/algocode/assets/109282492/766f01f7-e97a-4aa7-858a-d7dddbf89b7d)
<br/>
<br/>

<br/>

</details><br/>

<a href="https://www.linux.org/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="Linux" height="40" width="40" />
</a>
<a href="https://postman.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="Postman" height="40" width="40" />
</a>
<a href="https://www.w3schools.com/cpp/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" alt="C++" height="40" width="40" />
</a>
<a href="https://www.java.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/java/java-original.svg" alt="Java" height="40" width="40" />
</a>
<a href="https://www.python.org" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" height="40" width="40" />
</a>
<a href="https://www.djangoproject.com/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="Django" height="40" width="40" />
</a>
<a href="https://aws.amazon.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="AWS" height="40" width="40" />
</a>
<a href="https://www.docker.com/" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="Docker" height="40" width="40" />
</a>
<a href="https://www.gnu.org/software/bash/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/gnu_bash/gnu_bash-icon.svg" alt="Bash" height="40" width="40" />
</a>
<a href="https://azure.microsoft.com/en-in/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="Azure" height="40" width="40" />
</a>
<a href="https://circleci.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/circleci/circleci-icon.svg" alt="CircleCI" height="40" width="40" />
</a>
<a href="https://nodejs.org" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="Node.js" height="40" width="40" />
</a>
<a href="https://kafka.apache.org/" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="Kafka" height="40" width="40" />
</a>
<a href="https://www.rabbitmq.com" target="blank">
<img align="center" src="https://www.vectorlogo.zone/logos/rabbitmq/rabbitmq-icon.svg" alt="RabbitMQ" height="40" width="40" />
</a>
<a href="https://www.nginx.com" target="blank">
<img align="center" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="Nginx" height="40" width="40" />
</a>
<br/>

#### 🔗 Links

[![Email Me](https://img.shields.io/badge/mahboob-black?style=flat&logo=gmail)](mailto:connect.mahboobalam@gmail.com?subject=Hello) 
  <a href="https://twitter.com/imahboob_a" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-05122A?style=flat&logo=twitter&logoColor=white" alt="Twitter">
  </a>
  <a href="https://linkedin.com/in/i-mahboob-alam" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-05122A?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://hashnode.com/@imehboob" target="_blank">
    <img src="https://img.shields.io/badge/Hashnode-05122A?style=flat&logo=hashnode&logoColor=white" alt="Hashnode">
  </a>
  <a href="https://medium.com/@imehboob" target="_blank">
    <img src="https://img.shields.io/badge/Medium-05122A?style=flat&logo=medium&logoColor=white" alt="Medium">
  </a>
  <a href="https://dev.to/imahboob_a" target="_blank">
    <img src="https://img.shields.io/badge/Dev.to-05122A?style=flat&logo=dev.to&logoColor=white" alt="Devto">
  </a>
  <a href="https://www.leetcode.com/mahboob-alam" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-05122A?style=flat&logo=leetcode&logoColor=white" alt="LeetCode">
  </a>
<br/>