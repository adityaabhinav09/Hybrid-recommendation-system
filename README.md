# Hybrid Recommendation System

A configurable hybrid music recommendation system combining collaborative filtering and content-based techniques. This repository includes data processing, model artifacts, a Streamlit demo app, CI/CD workflow, and deployment scripts for AWS.

## Features
- Collaborative filtering pipeline
- Content-based filtering pipeline
- Hybrid recommendation fusion
- Data cleaning and transformation scripts
- Streamlit demo application (`app.py`)
- CI/CD workflow for testing and deploying to AWS (GitHub Actions)

## Repository Structure

- `app.py` — Streamlit app to demo recommendations
- `hybrid_recommendations.py` — combines collaborative and content-based models
- `collaborative_filtering.py` — collaborative filtering implementation
- `content_based_filtering.py` — content-based filtering implementation
- `data_cleaning.py` — data cleaning utilities
- `transform_filtered_data.py` — data transformation pipeline
- `transformer.joblib` — saved preprocessing transformer
- `data/` — datasets and preprocessed artifacts
- `deploy/` — deployment scripts
- `.github/workflows/ci.yaml` — CI pipeline
- `requirements.txt` — Python dependencies
- `test_app.py`, `test.py` — tests

## Setup

Prerequisites

- Python 3.10+ (virtualenv or venv recommended)
- Git
- (Optional) Docker for container builds

Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate     # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

If the project uses DVC for large data files, pull the data before running the app:

```bash
dvc pull
```

## Run the Streamlit Demo

Start the demo locally:

```bash
streamlit run app.py --server.port 8080
```

Open http://localhost:8080 in your browser.

## Running Tests

Run tests with pytest:

```bash
pytest -q
```

## Building and Pushing Docker Image (CI)

The repository includes a GitHub Actions workflow at `.github/workflows/ci.yaml` that builds and pushes a Docker image to Amazon ECR. Locally, you can build the image with:

```bash
docker build -t hybrid-recsys:latest .
```

## CI/CD (GitHub Actions)

This repository includes a GitHub Actions workflow at [.github/workflows/ci.yaml](.github/workflows/ci.yaml) which automates testing, container build, and deployment packaging. The workflow is configured to run for pushes and pull requests targeting the `main` branch.

Summary of the workflow steps:

- Checkout the repository and set up Python (uses `actions/checkout` and `actions/setup-python`).
- Install Python dependencies from `requirements.txt`.
- Configure AWS credentials (reads GitHub Secrets) and run `dvc pull` to fetch data artifacts.
- Start the Streamlit demo (the workflow runs the app on port `8000`), wait, then run the test suite (`pytest test_app.py`) and stop the app.
- Configure AWS credentials for ECR, log in to Amazon ECR, build and push a Docker image.
- Package deployment artifacts (appspec and scripts) into `deployment.zip` and upload the ZIP to an S3 bucket.
- Optionally, the workflow contains commands to create a CodeDeploy deployment (the commands can be enabled as needed).

Required GitHub Secrets and configuration:

- `AWS_ACCESS_KEY_ID` — AWS access key ID used by Actions to authenticate.
- `AWS_SECRET_ACCESS_KEY` — AWS secret access key used by Actions to authenticate.
- `ECR_REPOSITORY_URI` — target ECR repository URI used by the workflow when tagging and pushing the image.
- A reachable DVC remote (if the repository uses DVC) with credentials configured in the CI environment or available via the AWS credentials above.

Notes and recommendations:

- Ensure a `main` branch exists in the remote repository and that the workflow file is present at [.github/workflows/ci.yaml](.github/workflows/ci.yaml). To create and push `main` locally:

```bash
git checkout -b main
git push -u origin main
```

- The workflow starts the Streamlit server on port `8000` during CI; the local development default here is `8080` (see Run the Streamlit Demo). If the port needs to be changed in CI, update the command in the workflow.
- Keep secrets in GitHub repository settings (Settings → Secrets and variables → Actions) — do not store secrets in code.
- The CodeDeploy step is present but can be left commented out or enabled when the target CodeDeploy application and deployment group are ready.

For full details, review the workflow at [.github/workflows/ci.yaml](.github/workflows/ci.yaml).

## Deployment

Deployment scripts are in the `deploy/scripts/` folder. The CI workflow zips these artifacts and uploads them to S3 for AWS CodeDeploy.

## Notes & Tips

- If you add or update large data files, use DVC to track and push them to the remote.
- Manage secrets (AWS keys, ECR repository) with GitHub Secrets when using Actions.
- To speed up development iteration, run the parts you are working on (for example, run `hybrid_recommendations.py` functions in an interactive REPL or notebook).

## Contributing

Contributions are welcome. Please open issues or pull requests with a clear description of changes and tests where appropriate.

## License

## Author
 Aditya Abhinav