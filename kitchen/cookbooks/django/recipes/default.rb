#
# Cookbook:: django
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.

virtual_environment = "/opt/django/venv"
project_name = "testapp"

# Setup environment
python_runtime '3'

python_virtualenv virtual_environment

python_package 'Django' do
    version '1.10'
end

include_recipe 'django::startproject'
include_recipe 'django::deploy'

