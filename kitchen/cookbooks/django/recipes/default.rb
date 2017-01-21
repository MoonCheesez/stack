#
# Cookbook:: django
# Recipe:: default
#
# Copyright:: 2017, The Authors, All Rights Reserved.

# for ease of use
package 'vim'

include_recipe 'django::setup_user'
include_recipe 'django::setup_env'

include_recipe 'django::startproject'
include_recipe 'django::deploy'