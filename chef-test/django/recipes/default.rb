#
# Cookbook:: django
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.

include_recipe 'poise-python'

# Install python 3
python_runtime '3'
# Create a virtual environment
python_virtualenv '/opt/djangoapp/venv'

# Install django
python_package 'Django' do
    version '1.10'
end
