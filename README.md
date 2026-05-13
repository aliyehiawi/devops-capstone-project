# DevOps Capstone Project

[![Build Status](https://github.com/aliyehiawi/devops-capstone-project/actions/workflows/ci-build.yml/badge.svg)](https://github.com/aliyehiawi/devops-capstone-project/actions/workflows/ci-build.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/python-3.9-green.svg)](https://shields.io/)

This repository contains the capstone project for the **IBM DevOps and Software Engineering Professional Certificate**. It implements a RESTful Account service developed using Test Driven Development, secured with security headers and CORS, containerized with Docker, deployed to Kubernetes, and automated through a CI pipeline (GitHub Actions) and a CD pipeline (Tekton).

## Project layout

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/user-story.md   # User story template
│   └── workflows/ci-build.yml         # GitHub Actions CI workflow
├── service/
│   ├── __init__.py                    # Flask app factory + Talisman + CORS
│   ├── config.py                      # App configuration
│   ├── models.py                      # Account SQLAlchemy model
│   ├── routes.py                      # REST endpoints
│   └── common/                        # Shared helpers
├── tests/
│   ├── factories.py                   # Test data factories
│   ├── test_models.py                 # Model unit tests
│   └── test_routes.py                 # Route unit tests
├── tekton/
│   ├── tasks.yaml                     # Tekton custom tasks
│   └── pipeline.yaml                  # CD pipeline definition
├── Dockerfile                         # Container build
├── requirements.txt                   # Python dependencies
└── setup.cfg                          # nosetests / coverage / flake8 / pylint
```

## Running locally

```bash
pip install -r requirements.txt
honcho start
```

The service listens on port `8080` and exposes `/accounts` for CRUD operations.

## License

Apache 2.0. See [LICENSE](LICENSE).
