# Send NASA APOD Email

This AWS Lambda function fetches the NASA Astronomy Picture of the Day (APOD) and sends it via email using SendGrid. It includes a visually appealing email template with dynamic content, such as greetings, descriptions, mysterious content, and space facts.


## Features

- Fetches APOD data from NASA's API.
- Sends emails using SendGrid with a customizable HTML template.
- Generates dynamic greetings based on the day counter.
- Includes mysterious content and a space fact of the day.
- Supports multiple recipients defined in environment variables.

## Prerequisites

Before deploying this Lambda function, ensure you have the following:

- An AWS account with permissions to create Lambda functions and IAM roles.
- A SendGrid account with an API key.
- Verified sender email addresses in [SendGrid](https://sendgrid.com/en-us/solutions/email-api).

## Environment Variables

Make sure to set the following environment variables in your Lambda function:

- `SENDGRID_API_KEY`: Your SendGrid API key.
- `NASA_API_KEY`: Your NASA API key.
- `SENDER_EMAIL`: The email address from which the email will be sent (must be verified in SendGrid).
- `RECIPIENTS`: A comma-separated list of email addresses to receive the APOD.

## Template Overview

The email template includes:

- A catchy subject line: `Cosmic Journey - Day {#day}: Today's NASA Astronomy Picture of the Day!`
- Dynamic greetings chosen randomly based on the current day.
- The APOD image, title, and explanation.
- Additional mysterious content about space.
- A fact of the day related to space exploration.

## Usage

1. **Deploying the Lambda Function:**

   You can deploy the Lambda function using the AWS Management Console or using tools like the AWS CLI or AWS SAM. 

2. **Testing the Function:**

   You can test the function using the AWS Lambda console by providing a test event with the `recipients` field set to a list of email addresses.

3. **Scheduling the Function:**

   To send daily emails, set up a CloudWatch Events rule to trigger the Lambda function on a daily schedule.

## Acknowledgments
- NASA for providing the Astronomy Picture of the Day API.
- SendGrid for email delivery services.

## Credentials - Secrets
Credentials to properly deploy and test (as well initializing) this project should be inserted by the user. 

## Example Test Event

To test the Lambda function, you can use the following example event payload:

```
{
  "recipients": ["example@gmail.com"]
}
```

### Suggestion: 
You can get such bodies by asking track/playlist suggestion from ChatGPT in such format.

### Remote invoke test to trigger your lambda manually:
```
sam remote invoke --stack-name nasa-lambdas SendgridSendApodEmailFunction --event-file sendgrid-send-apod-email/events/test-event.json
```

## Note:
Could have achieved the same functionality by sending the email with AWS Simple Email Service (SES) instead.
However, it was noticed that there was a considerable delay when the email was sent with SES in contrast to SendGrid,
so this why this integration was used. 
