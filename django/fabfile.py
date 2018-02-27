from fabric.api import local

def webpack():
    local('rm -rf www/static/bundles/stage/*')
    local('rm -rf www/static/bundles/prod/*')
    local('rm -rf www/static/bundles/local/*')
    local('webpack --config webpack.stage.config.js --progress --colors')
    local('webpack --config webpack.local.config.js --progress --colors')
    local('webpack --config webpack.prod.config.js --progress --colors')
