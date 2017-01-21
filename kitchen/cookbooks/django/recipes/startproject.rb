#
# Cookbook:: django
# Recipe:: startproject
#
# Copyright:: 2017, The Authors, All Rights Reserved.

name = node.default['django']['project_name']
venv = node.default['django']['virtual_env']
# Create the environment directory
directory "#{venv}/#{name}/#{name}" do
    recursive true
end

# Add manage.py
template "#{venv}/#{name}/manage.py" do
    source 'manage.py.erb'
    variables project: "#{name}"
end

# Setting files
['settings.py', 'urls.py', 'wsgi.py'].each do |setting_file|
    template "#{venv}/#{name}/#{name}/#{setting_file}" do
        source "#{setting_file}.erb"
        variables project: "#{name}"
    end
end

# Create __init__.py file
file "#{venv}/#{name}/#{name}/__init__.py"