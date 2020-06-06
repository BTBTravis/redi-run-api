#!/usr/bin/env bash
npx redoc-cli bundle openapi.yaml
mv ./redoc-static.html ./docs