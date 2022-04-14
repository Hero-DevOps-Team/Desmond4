TOPIC 1 - CLOUDFORMATION
Lab 1.1.1
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-1-1stack/ad84c560-a85c-11ec-b66b-0a7f234b925f
Lab 1.1.2
Stack ID :arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-2-2stack/c3548920-a875-11ec-8555-120f8414fb73
Lab 1.1.3
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-1-3stack/4b308630-a864-11ec-bb1e-0af63ef8ea67
Lab 1.1.4
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-1-4stack/e11b4720-a864-11ec-aa40-0e9b4dd12971
Lab 1.1.5
Stack ID : lab1-1-4stack
What happens when i try to delete the stack from AWS CLI which i've just enabled the termination protection, using the command --> aws cloudformation delete-stack --stack-name stacksintelligent , i got the following message --> An error occurred (AccessDenied) when calling the DeleteStack operation: User: arn:aws:iam::324320755747:user/desmond.ndambi.labs is not authorized to perform: cloudformation:DeleteStack on resource: arn:aws:cloudformation:us-east-1:324320755747:stack/stacksintelligent/7375caf0-a57c-11ec-8454-0e4b061813b3 with an explicit deny in an identity-based policy

Trying to delete it from the AWS GUI yields this message --> "Termination protection is enabled on this stack. You must first disable termination protection on this stack before deleting it"

Lab 1.2.1
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-2-1stack/d1a56110-a871-11ec-a560-0a29a76cd5b1
Lab 1.2.2
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/lab1-2-2stack/c3548920-a875-11ec-8555-120f8414fb73
Lab 1.2.3
Stack ID : arn:aws:cloudformation:us-east-1:324320755747:stack/stackup/fb1cdc70-a877-11ec-8a6e-0a1ede6fec23
Lab 1.2.4
Some stacks are still under ROLLBACK

Lab 1.3.1
Url: link-to-the-PowerShell-script

Lab 1.3.2
Url : Python Version for stack creation

Lab 1.3.3
AWS CLI : --> aws s3 ls
