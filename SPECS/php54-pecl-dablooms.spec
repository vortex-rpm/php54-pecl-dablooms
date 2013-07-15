%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%global php_base php54
%global pecl_name dablooms
%global real_name dablooms

%global _version 0.9.1

Summary: A Scalable, Counting, Bloom Filter
Name: %{php_base}-pecl-dablooms

Version: %{_version}
Release: 1.vortex%{?dist}
License: PHP
Group: Development/Languages
Vendor: Vortex RPM
URL: https://github.com/bitly/dablooms

Source0: %{pecl_name}-%{_version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-devel, %{php_base}-cli, %{php_base}-pear
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if %{?php_zend_api}0
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: %{php_base}-api = %{php_apiver}
%endif

%description
This project aims to demonstrate a novel bloom filter implementation that
can scale, and provide not only the addition of new members, but reliable
removal of existing members.

Bloom filters are a probabilistic data structure that provide
space-efficient storage of elements at the cost of possible false
positive on membership queries.

dablooms implements such a structure that takes additional metadata to
classify elements in order to make an intelligent decision as to which
bloom filter an element should belong.


%prep 
%setup -q -n %{pecl_name}-%{_version}


%build
cd phpdablooms
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd phpdablooms
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%clean
%{__rm} -rf %{buildroot}



%postun
if [ $1 -eq 0 ]; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so


%changelog
* Mon Jul 15 2013 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 0.9.1-1.vortex
- Initial packaging.

