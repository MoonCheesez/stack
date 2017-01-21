#
# Cookbook:: django
# Recipe:: setup_user
#
# Copyright:: 2017, The Authors, All Rights Reserved.

user node.default['django']['user']
group node.default['django']['group'] do
    action :create
    members node.default['django']['user']
end
