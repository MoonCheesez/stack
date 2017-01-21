#
# Cookbook:: uwsgi
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.


venv = node.default['django']['virtual_env']
name = node.default['django']['project_name']

python_package 'uwsgi' do
    virtualenv venv
end

# uwsgi directory
directory "#{venv}/#{name}/.uwsgi/" do
    recursive true
    owner 'vagrant'
    group 'vagrant'
end

# uwsgi ini
template "#{venv}/#{name}/.uwsgi/#{name}.ini" do
    source 'uwsgi.ini.erb'
    variables({
        base_directory: "#{venv}/#{name}",
        wsgi_file: "#{venv}/#{name}/#{name}/wsgi.py",
        home_directory: venv
    })
end

# uwsgi_params
uwsgi_params = "#{venv}/#{name}/.uwsgi/uwsgi_params"
node.default['uwsgi']['uwsgi_params'] = uwsgi_params

cookbook_file uwsgi_params do
    source 'uwsgi_params'
end

# Change permissions
user = node.default['django']['user']
group = node.default['django']['group']
venv = node.default['django']['virtual_env']
execute "chown-venv" do
    command "chown -R #{user}:#{group} #{venv}"
    user 'root'
end


# # uwsgi conf
# template "/etc/init/#{name}.conf" do
#     source 'uwsgi_service.conf.erb'
#     variables({
#         project_name: name,
#         virtual_env: venv
#     })
# end

# service "#{name}" do
#     provider Chef::Provider::Service::Upstart
#     supports status: true, restart: true, reload: true
#     action [:enable, :start]
# end
