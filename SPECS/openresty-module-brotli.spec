%if (0%{?rhel} == 7 || 0%{?rhel} == 8)
%define epoch 1
Epoch: %{epoch}
%endif

%define main_version        1.21.4.1
%define main_release        %{epoch}%{dist}.ngx
%define module_version      1.0.0rc
%define brotli_version      1.0.9

Name:           openresty-module-brotli
Version:        %{main_version}+%{module_version}
Release:        1%{?dist}
BuildArch:      x86_64
Summary:        OpenResty module for Brotli compression
Requires:       openresty = %{main_version}
License:        BSD

Source0:       https://openresty.org/download/openresty-%{main_version}.tar.gz
Source100:     https://github.com/google/ngx_brotli/archive/refs/tags/v%{module_version}.tar.gz
Source101:     https://github.com/google/brotli/archive/refs/tags/v%{brotli_version}.tar.gz

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl, systemtap-sdt-devel, git
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-pcre-devel >= 8.45-1

%define orprefix            %{_usr}/local/openresty
%define zlib_prefix         %{orprefix}/zlib
%define pcre_prefix         %{orprefix}/pcre
%define openssl_prefix      %{orprefix}/openssl111

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods. It is
similar in speed with deflate but offers more dense compression.

ngx_brotli is a set of two nginx modules:
* ngx_brotli filter module - used to compress responses on-the-fly,
* ngx_brotli static module - used to serve pre-compressed files.

%define bdir %{_builddir}/openresty-%{main_version}
%define NGINX_BUILDSTRING $(openresty -V 2>&1 | grep 'configure arguments' | sed "s#configure arguments:##g")

%prep
%setup -q -n "openresty-%{main_version}"
%setup -q -b 100 -n "ngx_brotli-%{module_version}"
%setup -q -b 101 -n "brotli-%{brotli_version}"
rm -rf %{_builddir}/ngx_brotli-%{module_version}/deps/brotli
cp -R %{_builddir}/brotli-%{brotli_version} %{_builddir}/ngx_brotli-%{module_version}/deps/brotli

%build
cd %{bdir}
./configure \
   --prefix="%{orprefix}" \
   --with-cc='ccache gcc -fdiagnostics-color=always' \
   --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include" \
   --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
   --with-pcre-jit \
   --without-http_rds_json_module \
   --without-http_rds_csv_module \
   --without-lua_rds_parser \
   --with-stream \
   --with-stream_ssl_module \
   --with-stream_ssl_preread_module \
   --with-http_v2_module \
   --without-mail_pop3_module \
   --without-mail_imap_module \
   --without-mail_smtp_module \
   --with-http_stub_status_module \
   --with-http_realip_module \
   --with-http_addition_module \
   --with-http_auth_request_module \
   --with-http_secure_link_module \
   --with-http_random_index_module \
   --with-http_gzip_static_module \
   --with-http_sub_module \
   --with-http_dav_module \
   --with-http_flv_module \
   --with-http_mp4_module \
   --with-http_gunzip_module \
   --with-threads \
   --with-compat \
   --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
   --add-dynamic-module=%{_builddir}/ngx_brotli-%{module_version} \
   -j`nproc`
cd %{_builddir}/openresty-%{main_version}/build/nginx-* && make modules -j`nproc`

%install
mkdir -p %{buildroot}%{orprefix}/nginx/modules
for so in `find %{bdir}/build/nginx-*/objs/ -maxdepth 1 -type f -name "*.so"`; do
%{__install} -m755 $so \
   %{buildroot}%{orprefix}/nginx/modules
done

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{orprefix}/nginx/modules/ngx_http_brotli_filter_module.so
%{orprefix}/nginx/modules/ngx_http_brotli_static_module.so