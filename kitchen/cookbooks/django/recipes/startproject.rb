#
# Cookbook:: django
# Recipe:: startproject
#
# Copyright:: 2017, The Authors, All Rights Reserved.

project_name = node.default['django']['project_name']
env = node.default['django']['env']
# Create the environment directory
directory "#{env}/#{project_name}/#{project_name}" do
    recursive true
end

# Add manage.py
template "#{env}/#{project_name}/manage.py" do
    source 'manage.py.erb'
    variables project: "#{project_name}"
end

# Setting files
['settings.py', 'urls.py', 'wsgi.py'].each do |setting_file|
    template "#{env}/#{project_name}/#{project_name}/#{setting_file}" do
        source "#{setting_file}.erb"
        variables project: "#{project_name}"
    end
end

# Create __init__.py file
file "#{env}/#{project_name}/#{project_name}/__init__.py"