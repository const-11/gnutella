#!/bin/bash

pushd ./shared_files
python -m SimpleHTTPServer 8000 &> /dev/null &
popd