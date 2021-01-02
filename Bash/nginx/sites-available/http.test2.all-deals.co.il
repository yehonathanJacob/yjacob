server {
    listen      80;             # port
    server_name test2.all-deals.co.il; # dns server name
    
    # log files
    access_log  /var/log/nginx/all-deals.co.il_access.log;
    error_log   /var/log/nginx/all-deals.co.il_error.lg;

    # document root where files stores for test.yjacob.net domain
    root /home/yjacob/tmp/nginx_game/all_deals;
 
    index index.html index.html;
}
