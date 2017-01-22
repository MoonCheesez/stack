#
# Cookbook:: uwsgi
# Recipe:: content
#
# Copyright:: 2017, The Authors, All Rights Reserved.

env = node.default['django']['env']
project_name = node.default['django']['project_name']

# uwsgi directory
directory "#{env}/#{project_name}/.uwsgi/" do
    recursive true
    owner 'vagrant'
    group 'vagrant'
end

# uwsgi ini
template "#{env}/#{project_name}/.uwsgi/#{project_name}.ini" do
    source 'uwsgi.ini.erb'
    variables({
        base_directory: "#{env}/#{project_name}",
        wsgi_file: "#{env}/#{project_name}/#{project_name}/wsgi.py",
        home_directory: env
    })
end

# uwsgi_params
uwsgi_params = "#{env}/#{project_name}/.uwsgi/uwsgi_params"
node.default['uwsgi']['uwsgi_params'] = uwsgi_params

cookbook_file uwsgi_params do
    source 'uwsgi_params'
end

# Change permissions
user = node.default['django']['user']
group = node.default['django']['group']
execute "chown-env" do
    command "chown -R #{user}:#{group} #{env}"
    user 'root'
end