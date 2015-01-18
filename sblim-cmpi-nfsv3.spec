Summary:	SBLIM CMPI NFSv3 instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe NFSv3 dla SBLIM CMPI
Name:		sblim-cmpi-nfsv3
Version:	1.1.1
Release:	4
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	7f590fda1835f22b935d8fbe64fde79f
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI NFSv3 providers.

%description -l pl.UTF-8
Dostawcy informacji NFSv3 dla SBLIM CMPI.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi \
	--disable-static

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.la
# API not exported
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_NFSv3System{Configuration,Setting}.registration \
	-m %{_datadir}/%{name}/Linux_NFSv3System{Configuration,Setting}.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_NFSv3System{Configuration,Setting}.registration \
		-m %{_datadir}/%{name}/Linux_NFSv3System{Configuration,Setting}.mof >/dev/null
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README README.TEST
%attr(755,root,root) %{_libdir}/libLinux_NFSv3SystemConfigurationUtil.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv3SettingContext.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv3SystemConfiguration.so
%attr(755,root,root) %{_libdir}/cmpi/libLinux_NFSv3SystemSetting.so
%dir %{_datadir}/sblim-cmpi-nfsv3
%{_datadir}/sblim-cmpi-nfsv3/Linux_NFSv3SystemConfiguration.mof
%{_datadir}/sblim-cmpi-nfsv3/Linux_NFSv3SystemConfiguration.registration
%{_datadir}/sblim-cmpi-nfsv3/Linux_NFSv3SystemSetting.mof
%{_datadir}/sblim-cmpi-nfsv3/Linux_NFSv3SystemSetting.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-nfsv3/provider-register.sh
