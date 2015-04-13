%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global pypi_name gnocchi

Name:           gnocchi
Version:	1.0.0a1
Release:	1%{?dist}
Summary:        Gnocchi is a API to store metrics and index resources

Group:		Development/Languages
License:	Apache 2.0
URL:		http://github.com/openstack/gnocchi
Source0:	https://pypi.python.org/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:	python-setuptools

Requires:       numpy
Requires:       python-oslo-config
Requires:       python-oslo-sphinx
Requires:       python-oslo-messaging
Requires:       python-pandas
Requires:       python-flask
Requires:       python-swiftclient
Requires:       python-pecan
Requires:       python-futures
Requires:       python-requests
Requires:	python-six
Requires:	python-sqlalchemy
Requires:	python-stevedore
Requires:	python-voluptuous
Requires:	python-werkzeug
Requires:	python-jinja2
Requires:	PyYAML
Requires:	python-sysv_ipc
Requires:	python-msgpack
Requires:	python-trollius
Requires:       python-retrying
Requires:       pytz

#TODO: tooz, pytimeparse, future, oslo.db, oslo.utils, oslo.serialization

%description
HTTP API to store metrics and index resources.

%prep
%setup -q

%build

%{__python} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/gnocchi/
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/gnocchi/
mkdir -p %{buildroot}/%{_var}/log/%{name}

# Configuration
cp -R etc/gnocchi/policy.json %{buildroot}/%{_sysconfdir}/gnocchi

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc doc/source/*
%config(noreplace) %{_sysconfdir}/gnocchi/policy.json
%{python_sitelib}/gnocchi
%{python_sitelib}/*.egg-info
%{_bindir}/carbonara-create
%{_bindir}/carbonara-dump
%{_bindir}/carbonara-update
%{_bindir}/gnocchi-api
%{_bindir}/gnocchi-dbsync
%{_bindir}/gnocchi-statsd


%changelog
* Mon Apr 13 2015 Pradeep Kilambi <pkilambi@redhat.com> 1.0.0a1-1
- initial package release


