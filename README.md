# openresty-module-brotli
RPM packaging for [ngx_brotli](https://github.com/google/ngx_brotli) intendeed to be binary-compatible
with official OpenResty RPM packages.

## Installation
Install `openresty-extras` repository:
```
curl -s https://packagecloud.io/install/repositories/manoaratefy/openresty-extras/script.rpm.sh | sudo bash
```
Install the `openresty-module-brotli` package:
```
dnf -y install openresty-module-brotli
```
## Configuration
To use the module, you have to include the dynamic extensions by adding them into `/usr/local/openresty/nginx/conf/nginx.conf` (usually on the first lines):
```
load_module modules/ngx_http_brotli_filter_module.so;
load_module modules/ngx_http_brotli_static_module.so;
```
Then, you can configure the module as you want, such as:
```
brotli on;
brotli_comp_level 6;
brotli_types application/atom+xml application/javascript application/json application/rss+xml
    application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype
    application/x-font-ttf application/x-javascript application/xhtml+xml application/xml
    font/eot font/opentype font/otf font/truetype image/svg+xml image/vnd.microsoft.icon
    image/x-icon image/x-win-bitmap text/css text/javascript text/plain text/xml;
```
See [the module's documentation](https://github.com/google/ngx_brotli#ngx_brotli) for more details.
## License

    Copyright (C) 2002-2015 Igor Sysoev
    Copyright (C) 2011-2015 Nginx, Inc.
    Copyright (C) 2015 Google Inc.
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
