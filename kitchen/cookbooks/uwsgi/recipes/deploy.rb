#
# Cookbook:: uwsgi
# Recipe:: deploy
#
# Copyright:: 2017, The Authors, All Rights Reserved.


# # uwsgi conf
# template "/etc/init/#{project_name}.conf" do
#     source 'uwsgi_service.conf.erb'
#     variables({
#         project_project_name: project_name,
#         virtual_env: env
#     })
# end

# service "#{project_name}" do
#     provider Chef::Provider::Service::Upstart
#     supports status: true, restart: true, reload: true
#     action [:enable, :start]
# end
