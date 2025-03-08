#!/bin/bash

# Install dependencies (if not already installed)
pip install django djangorestframework

# Generate manifest entries
python manage.py generate_manifest