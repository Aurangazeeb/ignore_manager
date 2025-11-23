# Project Root Artifact Review

## Recommended .gitignore rules
1. node_modules/ : Node.js dependencies folder, typically large and recreated via package.json - (Existing)
2. __pycache__/ : Python bytecode cache, generated automatically - (Existing)
3. dist/ : Build output directory, contains generated bundles/artifacts - (Existing)

## Recommended .dockerignore rules
1. node_modules/ : Exclude Node.js dependencies to reduce Docker image size - (Existing)
2. __pycache__/ : Exclude Python bytecode cache files from Docker image - (Existing)
3. dist/ : Exclude build output directory to avoid copying unnecessary artifacts - (Existing)
4. *.pyc : Exclude Python bytecode files specifically - (Existing)