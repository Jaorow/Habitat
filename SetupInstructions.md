a set of instructions to set up and host a fastapi/react application on GCP

# Application Setup

### Backend
- Copy backend structure
- `mkdir backend`
- `python3 -m venv venv`
- start venv
- pip install


### Frontend
- `mkdir frontend`
- `npx create-react-app my-app`
- `build application`
- `npm run build`
- move build file into backend (or you could change the build path with this `"build": "BUILD_PATH=../backend/build react-scripts build",`)


App should now run with `uvicorn main:app --reload`, check it out in localhost


# Docker
for this current docker file ensure build command builds to backend dir with `"build": "BUILD_PATH=../backend/build react-scripts build",` in package.json 
copy this docker file and the command to run it from docker.sh

# Hosting 
Head to GCP and set up a new project and set up the following APIs

- Artifact Registry (artifactregistry.googleapis.com)
- Cloud Run (run.googleapis.com)
- IAM Credentials API (iamcredentials.googleapis.com)

### configure a WIP for github
https://github.com/google-github-actions/auth#preferred-direct-workload-identity-federation.

- TODO: replace ${PROJECT_ID} with your value below.

1. 
```
gcloud iam workload-identity-pools create "github" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```
2. 
```
gcloud iam workload-identity-pools describe "github" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
```
this should return `projects/123456789/locations/global/workloadIdentityPools/github`

3. 
```
gcloud iam workload-identity-pools providers create-oidc "my-repo" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github" \
  --display-name="My GitHub repo Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

4. 
```
gcloud iam workload-identity-pools providers describe "my-repo" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github" \
  --format="value(name)"
```