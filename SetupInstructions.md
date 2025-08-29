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

```
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  iamcredentials.googleapis.com \
  secretmanager.googleapis.com
```

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
this should return WIP_ID = `projects/123456789/locations/global/workloadIdentityPools/github`

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

5. 

```
gcloud config set project jaorow
```
```
echo -n "my-secret-value" | gcloud secrets create my-secret \
  --replication-policy="automatic" \
  --data-file=-
```
! These are case sensitive
WIP ID is what we printed before and repo must be case sensitive
```
gcloud secrets add-iam-policy-binding "my-secret" \
  --project="${PROJECT_ID}" \
  --role="roles/secretmanager.secretAccessor" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"
```

```
gcloud iam workload-identity-pools providers update-oidc "my-repo" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github" \
  --attribute-condition="assertion.repository == '${Github_Account}/${Repo}'"
```

create a service account
```
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer"
```

```
gcloud projects add-iam-policy-binding jaorow \
  --member="serviceAccount:github-deployer@jaorow.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```
```
gcloud secrets add-iam-policy-binding gcp-key \
  --project=${PROJECT_ID} \
  --member="serviceAccount:github-deployer@jaorow.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

create GCP artifact repo in GCP called app
enable IAM Service Account Credentials API




## Make the service public
```
gcloud run services add-iam-policy-binding app \
  --region australia-southeast1 \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --project jaorow
```