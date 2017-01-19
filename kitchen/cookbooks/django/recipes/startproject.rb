#
# Cookbook:: django
# Recipe:: startproject
#
# Copyright:: 2017, The Authors, All Rights Reserved.

# Create the environment directory
directory "#{}/#{}/#{}" do
    recursive true
end

# Add manage.py
template "#{}/#{}/manage.py" do
    source 'manage.py.erb'
    variabes project: "#{}"
end

# Setting files
['settings.py', 'urls.py', 'wsgi.py'].each do |setting_file|
    template "#{}/#{}/#{}/#{}" do
        source "#{setting_file}.erb"
        variables project: "#{}"
    end
end

# Create __init__.py file
file "#{}/#{}/#{}/__init__.py"

# Change permissions
execute "chown-venv" do
    command "chown -R vagrant:vagrant #{}"
    user 'root'
end
