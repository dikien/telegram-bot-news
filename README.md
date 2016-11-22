# Telegram Bot News
A tutorial on creating a Python Telegram bot using AWS Lambda with AWS API Gateway.

![Telegram Bot](https://github.com/dikien/telegram-bot-news/resources/yahoo-news.png)

## Setup
I am choosing Asia Pacific (Seoul) region for AWS Lambda and Asia Pacific (Seoul) region for AWS API Gateway.

### Telegram
1. Go to [Telegram Web](https://web.telegram.org/).
3. Start a chat with [@BotFather](https://telegram.me/BotFather).
4. Type "/start".
5. Type "/newbot" to create a new bot. I named my bot "YahooNewsDigest_bot".
6. Note the HTTP API access token that @BotFather will reply you after you created the bot.

### Checkout Code
```
$ git clone https://github.com/dikien/telegram-bot-news.git  
$ cd telegram-bot-news  
$ pip install -t ./ -r requirements.txt
$ zip -r telegram-bot-news.zip * -x ./venv/\* .git/\*
```

### Configuring an AWS IAM role
As with anything AWS-related, you need an IAM role with access to specific resources and must give it a set of execution permissions before anything starts working properly. If you are like me, configuring IAM permissions is by far the most annoying part and is always where I stumble on new projects. To set one up that can run your Telegram bot, login to the [IAM console](https://aws.amazon.com/iam/ "AWS IAM console") and navigate to the "Roles" section. Create a new role. I name mine "lambda-gateway-execution-role." In the permissions section, attach the following policies to the role:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### AWS Lambda
1. Go to [AWS Lambda](https://ap-northeast-2.console.aws.amazon.com/lambda/home?region=ap-northeast-2).
2. Click "Get Started Now".
3. Under the "Select blueprint" screen, search for "hello-world"and you will see the hello-world blueprint which says "A starter AWS Lambda function.".
4. Click on "hello-world" (NOT "hello-world-python").
5. Click Next Button on Configure triggers
6. You will be brought to the "Configure Function" page.
7. Under "Name", you can choose any name for your function. I called it "telegram-bot-news".
8. Under "Runtime", ensure it is "Python 2.7".
9. Under "Code entry type", choose "Upload a .ZIP file" and click the "Upload" button" to browse for the file "telegram-bot-news.zip" which you have zipped previously.
10. Set Environment variables key for "Access_Token" and value for HTTP API access token
11. Under "Handler", we leave it as "yahoo.lambda_handler".
12. Under "Role", we choose "Basic Execution Role".
13. You will be brought to a "Role Summary" page.
14. Under "IAM Role", choose "lambda_basic_execution".
14. Under "Role Name", choose "oneClick_lambda_basic_execution_.....".
15. Click "Allow".
16. You will be brought back to the "Configure Function" page.
17. Leave "Memory (MB)" as "128MB".
18. You might want to increase "Timeout" to "8" seconds.
19. Under VPC, choose "No VPC".
20. Click "Next".
21. Click "Create function".

### AWS API Gateway
1. Go to [AWS API Gateway](https://ap-northeast-2.console.aws.amazon.com/apigateway/home?region=ap-northeast-2).
2. Click "Get Started Now".
3. Under "API name", enter the name of your API. I will just name it " Telegram Bot News".
4. Click "Create API".
5. You will be redirected to the "Resources" page.
6. Click "Create Method" and on the Actions dropdown menu on the left, choose "POST" and click on the "tick" icon.
7. Now, you will see the "/ - POST - Setup" page on the right.
8. Under "Integration Type", choose "Lambda Function".
9. Under "Lambda Region", choose "ap-northeast-2".
10. Under "Lambda Function", type "telegram" and it should auto-complete it to "telegram-bot-news".
11. Click "Save" and "Ok" when the popup appears.
12. You will be brought to the "/ - POST - Method Execution" Page.
13. Click "Integration Request".
14. Click "Body Mapping Templates" and the section should expand.
15. Click "When there are no templates defined"
16. Click "Add Mapping Template" and type in "application/json" and click on the "tick" icon.
17. Under "Input Passthrough" on the right, click on the "pencil" icon.
18. Choose "Mapping Template" on the dropdown that appears.
19. Copy and paste ```{"body": $input.json('$')}``` to the template box.
20. Click on the "tick" icon beside the dropdown once you are done.
21. Click on "Deploy API" button on the top left.
22. Under "Deployment Stage", click "New Stage".
23. Under "Stage Name", I will type in "production".
24. Click "Deploy".
25. Note the "Invoke URL" at the top and your API is now live.
26. To prevent DDoS, you can enable throttling. I changed from 1000 to 10 for Rate and 2000 to 20 for Burst.  

### Set Telegram Webhook
1. Replace &lt;ACCESS_TOKEN&gt; with your Telegram HTTP API access token obtained in the first step. 
2. Replace &lt;INVOKE_URL&gt; with your Invoke URL obtained in the previous step.
3. Run this command:
```
$ curl --data "url=<INVOKE_URL>" "https://api.telegram.org/bot<ACCESS_TOKEN>/setWebhook"
```
You should get back a response similar to this:
```
$ {"ok":true,"result":true,"description":"Webhook was set"}
```

### Delete Telegram Webhook
1. Replace &lt;ACCESS_TOKEN&gt; with your Telegram HTTP API access token obtained in the first step. 
2. Run this command:
```
$ curl --data "url=" "https://api.telegram.org/bot<ACCESS_TOKEN>/setWebhook"
```
You should get back a response similar to this:
```
$ {"ok":true,"result":true,"description":"Webhook was deleted"}
```

### Manual Installation from source and push to the Lambda
1. Go to Terminal
2. Run this command: 
```$ cd ~/Downloads```
3. Run this command:
```$ git clone https://github.com/dikien/telegram-bot-news.git```
4. Run this command:
```$ cd telegram-bot-news```
5. Run this command:
```$ virtualenv venv```
6. Run this command:
```$ pip install -t ./ -r requirements.txt```
7. Run this command:
```$ source venv/bin/activate```
8. Run this command:
```$ pip install -t ./ -r requirements.txt```
9. Setup AWS Command Line Interface
```$ pip install awscli```
10. Enter Access Key ID/Secret Access Key
```$ aws configure```
11. Run this command:
```$ ./lambda_publish.sh```

## Commands
### Get News 
Usage: ```/news```

### See Also
[Telegram Bot using AWS API Gateway and AWS Lambda](https://github.com/lesterchan/telegram-bot)
[Skeleton code for quickly getting Python Telegram Bots up and running](https://github.com/mamcmanus/pytelebot)
[Telegram Bot can control Torrent system(Deluge) on Remote Server](https://github.com/seungjuchoi/telegram-control-deluge)
[Publishing Your Skill Code to Lambda via the Command Line Interface](https://developer.amazon.com/public/community/post/Tx1UE9W1NQ0GYII/Publishing-Your-Skill-Code-to-Lambda-via-the-Command-Line-Interface)