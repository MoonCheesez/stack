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

include_recipe 'startproject'
# Create files
# Create the directory for the django project
directory "#{virtual_environment}/#{project_name}/#{project_name}" do
    recursive true
end
# manage.py
template "#{virtual_environment}/#{project_name}/manage.py" do
    source 'manage.py.erb'
    variables project: "#{project_name}"
end
# settings files
django_setting_files = ["settings.py", "urls.py", "wsgi.py"]
django_setting_files.each do |file_name|
    template "#{virtual_environment}/#{project_name}/#{project_name}/#{file_name}" do
        source "#{file_name}.erb"
        variables project: "#{project_name}"
    end
end
# __init__.py
file "#{virtual_environment}/#{project_name}/#{project_name}/__init__.py"

# Change all the permissions accordingly
execute "chown-venv" do
    command "chown -R vagrant:vagrant #{virtual_environment}"
    user 'root'
end

# Deploy Django App
application "#{virtual_environment}/#{project_name}" do
    django do
        manage_path "#{virtual_environment}/#{project_name}/manage.py"
        debug true
        migrate true
    end
end
