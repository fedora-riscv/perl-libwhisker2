Name:           perl-libwhisker2
Obsoletes:      perl-libwhisker <= 1.8
Provides:       perl-libwhisker = %{version}-%{release}
Version:        2.4
Release:        6%{?dist}
Summary:        Perl module geared specificly for HTTP testing

Group:          Development/Libraries
License:        GPLv2+
URL:            http://www.wiretrip.net/rfp/lw.asp
Source0:        http://www.wiretrip.net/rfp/libwhisker/libwhisker2-%{version}.tar.gz
#install to vendorlib, not sitelib
Patch0:         libwhisker2-2.4-vendorlib.patch
#include libwhisker1 compatibility bridge
Patch1:         libwhisker2-2.4-lw1bridge.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl
Requires:       perl(Net::SSLeay), openssl-perl  
Requires:       perl(MD5)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Libwhisker is a Perl module geared specificly for HTTP testing.

%prep
%setup -qn libwhisker2-%{version}
%patch0 -p1
%patch1 -p1

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#create directories, not created by Makefile.pl
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3

make install DESTDIR=$RPM_BUILD_ROOT

#fix permissions
chmod 0644 $RPM_BUILD_ROOT/%{perl_vendorlib}/*

#%check
#cd t 
#perl ./test.pl

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4-4
Rebuild for new perl

* Wed May 23 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 2.4-3
- Fix patch to really include lw1 bridge
* Tue May 08 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 2.4-2
- Fix typo in Source0 url
- Update lw1bridge patch to not include License info
- Add explicit version to Provides and Obsoletes
- Added tests, commented out
- Cleaned up BuildRequires and Requires
* Fri May 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 2.4-1
- Initial build
