# System Requirements:
 - python3 
 - pip3

# Installation
  - Install allure commandline [installation guide](https://docs.qameta.io/allure/#_installing_a_commandline)  
  - Install the dependencies 
  ```sh
  pip3 install -r requirements.txt
  ```
### Used Plugins

| Plugin | README |
| ------ | ------ |
| selenium | To manipulate with browser|
| pytest | To run tests |
| pytest-xdist | To support parallel test run |
| webdriver-manager | To support different versions and type of browsers |
| allure-pytest | To integrate allure reporter with pytests |
| pytest-json-report | To generate json reports |


# How to run
 ```sh
$ python3 run.py  --browser chrome
 ```

### Run parameters
- ```--env``` - Set the environment in which tests will be run  
 -- Supported values ```live``` , ```new```  
 -- Default value ```live```

```sh
python3 run.py --env new
```
- ```--page``` - run speciific class tests  
 -- Supported values ```teacher-signup``` , ```teacher-classes```, ```teacher-curriculum```, ```teacher-order```, ```teacher-assignments```  
 -- No default value  
 -- Parameter is optional  
```sh
python3 run.py --page teacher-signup
```
- ```--browser``` - specify the browser in which tests will be run, please note that you can specify multiple browsers  
 -- Supported browsers ```chrome``` , ```firefox```, ```safari```, ```edge```  
 -- Default value ```chrome```  
 -- Parameter is optional  
```sh
python3 run.py --browser chrome firefox
```

```sh
python3 run.py --browser chrome
```

- ```--group``` - run specific group tests  
 -- All supported values are listed in ```pytest.ini``` file  
 -- No default value  
 -- Parameter is optional   
```sh
python3 run.py --group assignments
```
- ```--thread_count``` or ```-t``` - run tests in parallel  
 -- Supported int type values   
 -- Supported ```auto``` value to use as many processes as your computer has CPU cores   
 -- Parameter is optional   
```sh
python3 run.py -t 2
```

## Send test report to email  
By default this option is turned off, you can specify ```to_email``` parameter to turn on this option  
### Parameters:  
- ```--to_email``` to send email report to specified email address  
```sh
$ python3 run.py --to_email someexampleemail@test.com
```
- ```from_email``` specify sender email  
 -- By default it has value  
- ```--password``` specify sender password  
- ```--smtp_host``` specify SMTP host  
- ```--smtp_port``` specify SMTP port  

## Send test report to slack  
Please read how to create [Incoming Webhooks](https://api.slack.com/messaging/webhooks)  
By default this option is turned off, you can specify  
```--send_slack True``` to turn on this option  

### Parameters:
- ```--slack_hook``` specify the [Incoming Webhooks](https://api.slack.com/messaging/webhooks) url  

```sh
$ python3 run.py --send_slack True --slack_hook https://hooks.slack.com/services/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
```
