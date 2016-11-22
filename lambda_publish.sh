#!/usr/bin/env bash
rm telegram-bot-news.zip
zip -r telegram-bot-news.zip * -x ./venv/\* .git/\*
aws lambda update-function-code --function-name telegram-bot-news --zip-file fileb://telegram-bot-news.zip