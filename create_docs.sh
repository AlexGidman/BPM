#!/bin/bash

cd docs;
make clean html;
open build/html/index.html;
cd ..;