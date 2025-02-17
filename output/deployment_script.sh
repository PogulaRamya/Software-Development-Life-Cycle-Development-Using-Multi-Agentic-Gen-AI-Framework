Below is a bash deployment script for the given Python program:

```bash
#!/bin/bash

# This script deploys the given Python program in a specified environment.
# Usage:
#   ./deploy.sh [environment]
# Example:
#   ./deploy.sh production

# Step 1: Define environment variables
# Ensure these are set in the host system and not hardcoded for security reasons.
DB_USERNAME=$DB_USERNAME
DB_PASSWORD=$DB_PASSWORD
API_KEY=$API_KEY
ENV=$1  # The deployment environment (development, staging, production).

# Step 2: Validate dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but not installed.  Aborting."; exit 1; }

# Step 3: Validate inputs
if [ -z "$ENV" ]; then
  echo "Error: No environment provided."
  echo "Usage: ./deploy.sh [environment]"
  exit 1
fi

# Step 4: Deploy based on environment
if [ $ENV = "production" ]; then
  echo "Deploying to production..."
  # Production-specific commands here
elif [ $ENV = "staging" ]; then
  echo "Deploying to staging..."
  # Staging-specific commands here
elif [ $ENV = "development" ]; then
  echo "Deploying to development..."
  # Development-specific commands here
else
  echo "Error: Invalid environment '$ENV'. Choose from 'development', 'staging', or 'production'."
  exit 1
fi

# Step 5: Begin deployment
# Ensure idempotence by checking if application is already deployed before deployment

echo "Starting deployment..."
python3 -c 'import sys; print(sys.version_info[:])' >/dev/null 2>&1 ||
{
  echo >&2 "An error occurred while running the Python script. Aborting.";
  exit 1;
}

# Step 6: Cleanup
# Delete temporary files, kill unnecessary processes, etc.

# Step 7: End deployment
echo "Deployment successful!"

exit 0
```

Please make sure to replace placeholders with actual commands for production, staging, and development environments. The script checks the availability of Python3 and environment inputs before proceeding and includes error handling for graceful failure. It will not proceed further if Python3 is not installed or if no environment input is provided. Also, all sensitive information (DB username, password, and API key) are expected to be environment variables.