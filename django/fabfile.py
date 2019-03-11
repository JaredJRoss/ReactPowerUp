from fabric.api import local

def webpack():
    local('rm -rf www/static/bundles/stage/*')
    local('rm -rf djreact/static/bundles/stage/*')
    local('webpack --config webpack.stage.config.js --progress --colors')

