#
# Cookbook:: uwsgi
# Recipe:: deploy
#
# Copyright:: 2017, The Authors, All Rights Reserved.

project_name = node.default['django']['project_name']
env = node.default['django']['env']

# uwsgi conf
template '/etc/systemd/system/uwsgi.service' do
    source 'uwsgi.service.erb'
    variables({
        project_name: project_name,
        env: env
    })
end

service "uwsgi" do
    provider Chef::Provider::Service::Systemd
    supports status: true, restart: true, start: true, stop: true
    action [:enable, :restart]
end