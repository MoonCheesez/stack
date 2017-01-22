#
# Cookbook:: django
# Recipe:: deploy
#
# Copyright:: 2017, The Authors, All Rights Reserved.

env = node.default['django']['env']
project_name = node.default['django']['project_name']

application "#{env}/#{project_name}" do
    django do
        manage_path "#{env}/#{project_name}/manage.py"
        debug true
        migrate true
    end
end
