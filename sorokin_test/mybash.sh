#!/bin/bash

python manage.py model_list > $(date +%Y_%m_%d).dat 