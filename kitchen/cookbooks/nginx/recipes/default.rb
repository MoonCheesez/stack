#
# Cookbook:: nginx
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.

package 'nginx'

# Setup nginx config
venv = node.default['django']['virtual_env']
name = node.default['django']['project_name']

template "/etc/nginx/sites-enabled/#{name}_nginx.conf" do
    source 'nginx_conf.conf.erb'
    variables({
        socket: "#{venv}/#{name}/#{name}.sock",
        static_directory: "#{venv}/#{name}/static",
        uwsgi_params: node.default['uwsgi']['uwsg_params']
    })
end

# Start nginx
service 'nginx' do
    action [:enable, :start]
end

