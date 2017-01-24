#
# Cookbook:: nginx
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.

package 'nginx'

# Setup nginx config
env = node.default['django']['env']
project_name = node.default['django']['project_name']

template "/etc/nginx/sites-enabled/#{project_name}_nginx.conf" do
    source 'nginx_conf.conf.erb'
    variables({
        socket: "/tmp/uwsgi.socket",
        static_directory: "#{env}/#{project_name}/static",
        uwsgi_params: node.default['uwsgi']['uwsgi_params']
    })
end

# Start nginx
service 'nginx' do
    action [:enable, :restart]
end
