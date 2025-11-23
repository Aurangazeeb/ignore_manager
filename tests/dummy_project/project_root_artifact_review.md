```
# Project Root Artifact Review

## Recommended .gitignore rules
- [ ] node_modules/ # Node.js dependencies are installed and can be rebuilt, no need to include in version control.
- [ ] __pycache__/ # Python bytecode cache files are generated at runtime, should not be versioned.
- [ ] dist/ # Distribution/build output files are generated artifacts, not source code.

## Recommended .dockerignore rules
- [ ] node_modules/ # Avoid copying dependencies to keep Docker image lean; install within container as needed.
- [ ] __pycache__/ # Bytecode caches are unnecessary in the Docker image and increase size.
- [ ] dist/ # Build output can be recreated within the Docker build process to keep image minimal.
```