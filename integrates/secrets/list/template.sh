# shellcheck shell=bash

export INTEGRATES_SECRETS_LIST=(
  AWS_OPENSEARCH_HOST
  AWS_REDSHIFT_DBNAME
  AWS_REDSHIFT_HOST
  AWS_REDSHIFT_PASSWORD
  AWS_REDSHIFT_USER
  AZUREAD_OAUTH2_KEY
  AZURE_OAUTH2_REPOSITORY_APP_ID
  AZURE_OAUTH2_REPOSITORY_SECRET
  AZUREAD_OAUTH2_SECRET
  BITBUCKET_OAUTH2_KEY
  BITBUCKET_OAUTH2_SECRET
  BUGSNAG_API_KEY_BACK
  BUGSNAG_API_KEY_SCHEDULER
  CLOUDFRONT_ACCESS_KEY
  CLOUDFRONT_PRIVATE_KEY
  CLOUDFRONT_REPORTS_DOMAIN
  CLOUDFRONT_RESOURCES_DOMAIN
  DEBUG
  DYNAMODB_HOST
  DYNAMODB_PORT
  ENVIRONMENT
  BITBUCKET_OAUTH2_REPOSITORY_APP_ID
  BITBUCKET_OAUTH2_REPOSITORY_SECRET
  FERNET_TOKEN
  GITHUB_OAUTH2_APP_ID
  GITHUB_OAUTH2_SECRET
  GITLAB_OAUTH2_APP_ID
  GITLAB_OAUTH2_SECRET
  GOOGLE_OAUTH2_KEY
  GOOGLE_OAUTH2_SECRET
  JWT_ENCRYPTION_KEY
  JWT_SECRET
  JWT_SECRET_API
  JWT_SECRET_RS512
  JWT_SECRET_API_RS512
  JWT_SECRET_ES512
  JWT_SECRET_API_ES512
  MAIL_CONTINUOUS
  MAIL_COS
  MAIL_CTO
  MAIL_CXO
  MAIL_CUSTOMER_EXPERIENCE
  MAIL_CUSTOMER_SUCCESS
  MAIL_FINANCE
  MAIL_PRODUCTION
  MAIL_PROJECTS
  MAIL_REVIEWERS
  MAIL_TELEMARKETING
  MANDRILL_APIKEY
  MIXPANEL_API_SECRET
  MIXPANEL_API_TOKEN
  MIXPANEL_PROJECT_ID
  STARLETTE_SESSION_KEY
  STRIPE_API_KEY
  STRIPE_WEBHOOK_KEY
  TEST_GITHUB_API_TOKEN
  TEST_GITHUB_SSH_PRIVATE_KEY
  TEST_ORGS
  TEST_PROJECTS
  TWILIO_ACCOUNT_SID
  TWILIO_AUTH_TOKEN
  TWILIO_VERIFY_SERVICE_SID
  ZENDESK_EMAIL
  ZENDESK_SUBDOMAIN
  ZENDESK_TOKEN
)
