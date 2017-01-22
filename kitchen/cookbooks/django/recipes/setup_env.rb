#
# Cookbook:: django
# Recipe:: setup_env
#
# Copyright:: 2017, The Authors, All Rights Reserved.

python_runtime '3'

python_package 'Django' do
    version '1.10'
end