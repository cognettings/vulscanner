import os

try:
    CACHIX_AUTH_TOKEN = os.environ.get("CACHIX_AUTH_TOKEN")
    CI_COMMIT_REF_NAME = os.environ["CI_COMMIT_REF_NAME"]
    CI_COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
    CI_COMMIT_SHORT_SHA = CI_COMMIT_SHA[0:8]
    FI_AWS_OPENSEARCH_HOST = os.environ["AWS_OPENSEARCH_HOST"]
    FI_AWS_REDSHIFT_DBNAME = os.environ.get("AWS_REDSHIFT_DBNAME")
    FI_AWS_REDSHIFT_HOST = os.environ.get("AWS_REDSHIFT_HOST")
    FI_AWS_REDSHIFT_PASSWORD = os.environ.get("AWS_REDSHIFT_PASSWORD")
    FI_AWS_REDSHIFT_USER = os.environ.get("AWS_REDSHIFT_USER")
    FI_AZUREAD_OAUTH2_KEY = os.environ["AZUREAD_OAUTH2_KEY"]
    FI_AZUREAD_OAUTH2_SECRET = os.environ["AZUREAD_OAUTH2_SECRET"]
    FI_BITBUCKET_OAUTH2_KEY = os.environ["BITBUCKET_OAUTH2_KEY"]
    FI_BITBUCKET_OAUTH2_SECRET = os.environ["BITBUCKET_OAUTH2_SECRET"]
    FI_BUGSNAG_API_KEY_BACK = os.environ["BUGSNAG_API_KEY_BACK"]
    FI_BUGSNAG_API_KEY_SCHEDULER = os.environ["BUGSNAG_API_KEY_SCHEDULER"]
    FI_INTEGRATES_CRITERIA_COMPLIANCE = os.environ[
        "INTEGRATES_CRITERIA_COMPLIANCE"
    ]
    FI_INTEGRATES_CRITERIA_REQUIREMENTS = os.environ[
        "INTEGRATES_CRITERIA_REQUIREMENTS"
    ]
    FI_INTEGRATES_CRITERIA_VULNERABILITIES = os.environ[
        "INTEGRATES_CRITERIA_VULNERABILITIES"
    ]
    FI_INTEGRATES_REPORTS_LOGO_PATH = os.environ[
        "INTEGRATES_REPORTS_LOGO_PATH"
    ]
    FI_INTEGRATES_DB_MODEL_PATH = os.environ["INTEGRATES_DB_MODEL_PATH"]
    FI_ASYNC_PROCESSING_DB_MODEL_PATH = os.environ[
        "ASYNC_PROCESSING_DB_MODEL_PATH"
    ]
    FI_DEBUG = os.environ["DEBUG"]
    FI_DYNAMODB_HOST = os.environ["DYNAMODB_HOST"]
    FI_DYNAMODB_PORT = os.environ["DYNAMODB_PORT"]
    FI_EMAIL_TEMPLATES: str = os.environ["INTEGRATES_MAILER_TEMPLATES"]
    FI_ENVIRONMENT = os.environ["ENVIRONMENT"]
    FI_AZURE_OAUTH2_REPOSITORY_APP_ID = os.environ[
        "AZURE_OAUTH2_REPOSITORY_APP_ID"
    ]
    FI_AZURE_OAUTH2_REPOSITORY_SECRET = os.environ[
        "AZURE_OAUTH2_REPOSITORY_SECRET"
    ]
    FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID = os.environ[
        "BITBUCKET_OAUTH2_REPOSITORY_APP_ID"
    ]
    FI_BITBUCKET_OAUTH2_REPOSITORY_SECRET = os.environ[
        "BITBUCKET_OAUTH2_REPOSITORY_SECRET"
    ]
    FI_FERNET_TOKEN = os.environ["FERNET_TOKEN"]
    FI_GITHUB_OAUTH2_APP_ID = os.environ["GITHUB_OAUTH2_APP_ID"]
    FI_GITHUB_OAUTH2_SECRET = os.environ["GITHUB_OAUTH2_SECRET"]
    FI_GITLAB_OAUTH2_APP_ID = os.environ["GITLAB_OAUTH2_APP_ID"]
    FI_GITLAB_OAUTH2_SECRET = os.environ["GITLAB_OAUTH2_SECRET"]
    FI_GOOGLE_OAUTH2_KEY = os.environ["GOOGLE_OAUTH2_KEY"]
    FI_GOOGLE_OAUTH2_SECRET = os.environ["GOOGLE_OAUTH2_SECRET"]
    FI_JWT_ENCRYPTION_KEY = os.environ["JWT_ENCRYPTION_KEY"]
    FI_JWT_SECRET = os.environ["JWT_SECRET"]
    FI_JWT_SECRET_API = os.environ["JWT_SECRET_API"]
    FI_JWT_SECRET_RS512 = os.environ["JWT_SECRET_RS512"]
    FI_JWT_SECRET_API_RS512 = os.environ["JWT_SECRET_API_RS512"]
    FI_JWT_SECRET_ES512 = os.environ["JWT_SECRET_ES512"]
    FI_JWT_SECRET_API_ES512 = os.environ["JWT_SECRET_API_ES512"]
    FI_MAIL_CONTINUOUS = os.environ["MAIL_CONTINUOUS"]
    FI_MAIL_COS = os.environ["MAIL_COS"]
    FI_MAIL_CTO = os.environ["MAIL_CTO"]
    FI_MAIL_CXO = os.environ["MAIL_CXO"]
    FI_MAIL_CUSTOMER_EXPERIENCE = os.environ["MAIL_CUSTOMER_EXPERIENCE"]
    FI_MAIL_CUSTOMER_SUCCESS = os.environ["MAIL_CUSTOMER_SUCCESS"]
    FI_MAIL_FINANCE = os.environ["MAIL_FINANCE"]
    FI_MAIL_PRODUCTION = os.environ["MAIL_PRODUCTION"]
    FI_MAIL_PROJECTS = os.environ["MAIL_PROJECTS"]
    FI_MAIL_REVIEWERS = os.environ["MAIL_REVIEWERS"]
    FI_MAIL_TELEMARKETING = os.environ["MAIL_TELEMARKETING"]
    FI_MANDRILL_API_KEY = os.environ["MANDRILL_APIKEY"]
    FI_MIXPANEL_API_SECRET = os.environ["MIXPANEL_API_SECRET"]
    FI_MIXPANEL_API_TOKEN = os.environ["MIXPANEL_API_TOKEN"]
    FI_MIXPANEL_PROJECT_ID = os.environ["MIXPANEL_PROJECT_ID"]
    FI_STARLETTE_SESSION_KEY = os.environ["STARLETTE_SESSION_KEY"]
    FI_STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
    FI_STRIPE_WEBHOOK_KEY = os.environ["STRIPE_WEBHOOK_KEY"]
    FI_TEST_ORGS = os.environ["TEST_ORGS"]
    FI_TEST_PROJECTS = os.environ["TEST_PROJECTS"]
    FI_TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    FI_TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    FI_TWILIO_VERIFY_SERVICE_SID = os.environ["TWILIO_VERIFY_SERVICE_SID"]
    FI_ZENDESK_EMAIL = os.environ["ZENDESK_EMAIL"]
    FI_ZENDESK_SUBDOMAIN = os.environ["ZENDESK_SUBDOMAIN"]
    FI_ZENDESK_TOKEN = os.environ["ZENDESK_TOKEN"]
    LOG_LEVEL_CONSOLE: str | None = os.environ.get("LOG_LEVEL_CONSOLE")
    LOG_LEVEL_BUGSNAG: str | None = os.environ.get("LOG_LEVEL_BUGSNAG")
    LOG_LEVEL_WATCHTOWER: str | None = os.environ.get("LOG_LEVEL_WATCHTOWER")
    UNIVERSE_API_TOKEN: str | None = os.environ.get("UNIVERSE_API_TOKEN")
    STARTDIR = os.environ["STARTDIR"]

    # not secrets but must be environment vars
    BASE_URL = "https://app.fluidattacks.com"
    FI_AWS_REDSHIFT_PORT = 5439
    FI_AWS_REGION_NAME = "us-east-1"
    FI_AWS_S3_MAIN_BUCKET = (
        "integrates" if FI_ENVIRONMENT == "production" else "integrates.dev"
    )
    FI_AWS_S3_CONTINUOUS_REPOSITORIES = (
        "integrates.continuous-repositories"
        if FI_ENVIRONMENT == "production"
        else "integrates.dev"
    )
    FI_AWS_S3_PATH_PREFIX = os.environ.get("AWS_S3_PATH_PREFIX", "")
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise
