# Philosophy - Philosopher of the day Email

This AWS Lambda function sends daily emails about philosophers using dynamically generated content from OpenAI's GPT-4
model. It includes an aesthetically pleasing email template with engaging content, such as key philosophical concepts, 
summaries, and thought-provoking questions.

## Features

- Fetches dynamic content about philosophers from OpenAI's GPT-4 API. 
- Sends emails using SendGrid with a customizable HTML template. 
- Generates a brief summary of the philosopher’s philosophy. 
- Provides a list of key concepts and "Food for Thought" questions. 
- Supports multiple recipients defined in a JSON file stored in S3. 
- Removes the philosopher from the list once the email is successfully sent.

## Prerequisites

Before deploying this Lambda function, ensure you have the following:

- An AWS account with permissions to create Lambda functions and IAM roles.
- A SendGrid account with an API key.
- Verified sender email addresses in [SendGrid](https://sendgrid.com/en-us/solutions/email-api).
- A pre-populated S3 bucket with two JSON files:
  - recipients.json containing the list of email recipients. 
  - philosophers.json containing the list of philosophers.

## Environment Variables

Make sure to set the following environment variables in your Lambda function:

- `SENDGRID_API_KEY`: Your SendGrid API key.
- `NASA_API_KEY`: Your NASA API key.
- `SENDER_EMAIL`: The email address from which the email will be sent (must be verified in SendGrid).
- `RECIPIENTS`: A comma-separated list of email addresses to receive the APOD.
- `S3_RECIPIENTS_BUCKET`: The name of the S3 bucket containing the recipients.json file. 
- `S3_RECIPIENTS_FILE_KEY`: The key (file path) for the recipients.json file in S3. 
- `S3_PHILOSOPHERS_BUCKET`: The name of the S3 bucket containing the philosophers.json file. 
- `S3_PHILOSOPHERS_FILE_KEY`: The key (file path) for the philosophers.json file in S3.

## Template Overview

The email template includes:

- A subject line: Philosopher's Daily Reflection: {Philosopher Name} 
- The philosopher’s name, a summary of their philosophy, and key concepts. 
- A "Food for Thought" section with thought-provoking questions. 
- Customizable, fun footer content.

## Usage

1. **Deploying the Lambda Function:**

    You can deploy the Lambda function using the AWS Management Console or using tools like the AWS CLI or AWS SAM. 

2. **Testing the Function:**

    You can test the function using the AWS Lambda console by providing a test event with the `recipients` field set to 
a list of email addresses.

3. **Scheduling the Function:**

   To send daily emails, set up a CloudWatch Events rule to trigger the Lambda function on a daily schedule.

4. **Updating Recipients and Philosophers:** 

    You can update the recipient list or add new philosophers by modifying the recipients.json or philosophers.json 
files in S3.

## Acknowledgments
- OpenAI for GPT-4 API, which answers provide the dynamic content for each email.
- SendGrid for email delivery services.

## Credentials - Secrets
Credentials to properly deploy and test (as well initializing) this project should be inserted by the user. 

## Example Test Event

To test the Lambda function, you can use the following example event payload:

```
{
  "test": "test"
}
```

### Suggestion: 
You can get such bodies by asking track/playlist suggestion from ChatGPT in such format.

### Remote invoke test to trigger your lambda manually:
```
sam remote invoke --stack-name philosophy PhilosophyOTDEmailFunction --event-file philosophy-otd-email/events/test-event.json
```

## Note:
Could have achieved the same functionality by sending the email with AWS Simple Email Service (SES) instead.
However, it was noticed that there was a considerable delay when the email was sent with SES in contrast to SendGrid,
so this why this integration was used. 
