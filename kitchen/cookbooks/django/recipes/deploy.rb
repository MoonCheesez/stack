#
# Cookbook:: django
# Recipe:: deploy
#
# Copyright:: 2017, The Authors, All Rights Reserved.

venv = node.default['django']['virtual_env']
name = node.default['django']['project_name']

application "#{venv}/#{name}" do
    django do
        manage_path "#{venv}/#{name}/manage.py"
        debug true
        migrate true
    end
end
