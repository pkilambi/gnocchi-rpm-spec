%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:           openstack-gnocchi
Version:	1.0.0c1
Release:	1%{?dist}
Summary:        Gnocchi is a API to store metrics and index resources

Group:		Development/Languages
License:	APL 2.0
URL:		http://github.com/openstack/gnocchi
Source0:	https://pypi.python.org/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        %{pypi_name}-dist.conf
Source2:        %{pypi_name}.conf.sample
BuildArch:      noarch

BuildRequires:	python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-pbr
BuildRequires:  python2-devel


%description
HTTP API to store metrics and index resources.

%package -n     python-gnocchi
Summary:        OpenStack gnocchi python libraries
Group:          Applications/System

Requires:       numpy
Requires:       python-flask
Requires:       python-futures
Requires:	python-jinja2
Requires:	python-msgpack
Requires:       python-oslo-config
Requires:       python-oslo-db
Requires:       python-oslo-log
Requires:       python-oslo-policy
Requires:       python-oslo-sphinx
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-pandas
Requires:       python-pecan
Requires:       python-retrying
Requires:       python-requests
Requires:       python-swiftclient
Requires:	python-six
Requires:	python-sqlalchemy
Requires:	python-stevedore
Requires:	python-sysv_ipc
Requires:       python-tooz
Requires:	python-trollius
Requires:	python-voluptuous
Requires:	python-werkzeug
Requires:       pytz
Requires:	PyYAML
#TODO: Requires: pytimeparse, SQLAlchemy-Utils, python-oslo-db == 1.7, python-keystonemiddleware > 1.5, python-oslo-policy (on koji), pandas >= 0.15

%description -n   python-gnocchi
OpenStack gnocchi provides API to store metrics from OpenStack components
and index resources.

This package contains the gnocchi python library.


%package        api

Summary:        OpenStack gnocchi api
Group:          Applications/System

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-flask
Requires:       python-jinja2
Requires:       python-keystonemiddleware
Requires:       python-oslo-db
Requires:       python-oslo-policy
Requires:       python-oslo-utils
Requires:       python-oslo-serialization
Requires:       python-pecan
Requires:       python-requests
Requires:       python-six
Requires:       python-stevedore
Requires:       python-voluptuous
Requires:       python-werkzeug
Requires:       PyYAML

%description api
OpenStack gnocchi provides API to store metrics from OpenStack components
and index resources.

This package contains the gnocchi API service.

%package        carbonara

Summary:        OpenStack gnocchi carbonara
Group:          Applications/System

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-futures
Requires:       python-msgpack
Requires:       python-oslo-utils
Requires:       python-pandas
Requires:       python-retrying
Requires:       python-swiftclient
Requires:       python-tooz

%description carbonara
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi carbonara backend including swift,ceph and
file service.


%package        indexer-sqlalchemy

Summary:        OpenStack gnocchi indexer sqlalchemy driver
Group:          Applications/System

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-oslo-db
Requires:       python-oslo-utils
Requires:       python-sqlalchemy
Requires:       python-swiftclient
Requires:       python-stevedore
Requires:       pytz

%description indexer-sqlalchemy
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi indexer with sqlalchemy driver.


%package        statsd

Summary:        OpenStack gnocchi statsd daemon
Group:          Applications/System

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-oslo-log
Requires:       python-oslo-utils
Requires:       python-trollius
Requires:       python-six

%description statsd
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi statsd daemon

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack gnocchi
Group:            Documentation

Requires:         python-gnocchi = %{version}-%{release}

%description      doc
OpenStack gnocchi provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for gnocchi.
%endif


%prep
%setup -q -n gnocchi-%{version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find gnocchi -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build

%{__python} setup.py build

install -p -D -m 640 %{SOURCE2} etc/gnocchi/gnocchi.conf.sample

while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/gnocchi/gnocchi.conf.sample
done < %{SOURCE1}


%install
rm -rf %{buildroot}

%{__python} setup.py install --skip-build --root %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/gnocchi/
mkdir -p %{buildroot}/%{_sysconfdir}/ceilometer/
mkdir -p %{buildroot}/%{_var}/log/%{name}

install -p -D -m 640 etc/gnocchi/gnocchi.conf.sample %{buildroot}%{_sysconfdir}/gnocchi/gnocchi.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R etc/gnocchi/policy.json %{buildroot}/%{_sysconfdir}/gnocchi
cp -R etc/ceilometer/gnocchi_archive_policy_map.yaml %{buildroot}/%{_sysconfdir}/ceilometer

%clean
rm -rf %{buildroot}


%post -n %{name}-api
%systemd_post %{name}-api.service

%preun -n %{name}-api
%systemd_preun %{name}-api.service

%files -n python-gnocchi
%{python_sitelib}/gnocchi
%{python_sitelib}/gnocchi-%{version}*.egg-info

%files api
%defattr(-,root,root,-)
%dir %{_sysconfdir}/gnocchi
%config(noreplace) %{_sysconfdir}/gnocchi/policy.json
%config(noreplace) %{_sysconfdir}/gnocchi/gnocchi.conf
%config(noreplace) %{_sysconfdir}/ceilometer/gnocchi_archive_policy_map.yaml
%{_bindir}/gnocchi-api

%files carbonara
%{_bindir}/carbonara-create
%{_bindir}/carbonara-dump
%{_bindir}/carbonara-update

%files indexer-sqlalchemy
%{_bindir}/gnocchi-dbsync

%files statsd
%{_bindir}/gnocchi-statsd

%if 0%{?with_doc}
%files doc
%doc doc/source/
%endif


%changelog
* Mon Apr 22 2015 Pradeep Kilambi <pkilambi@redhat.com> 1.0.0c1-1
- initial package release


