%define real_name libwhisker2
Name:           perl-%{real_name}
Obsoletes:      perl-libwhisker <= 1.8
Provides:       perl-libwhisker = %{version}-%{release}
Version:        2.5
Release:        1%{?dist}
Summary:        Perl module geared specifically for HTTP testing

Group:          Development/Libraries
License:        BSD
URL:            http://www.wiretrip.net/rfp/lw.asp
Source0:        http://www.wiretrip.net/rfp/libwhisker/%{real_name}-%{version}.tar.gz
#install to vendorlib, not sitelib
Patch0:         %{real_name}-2.4-vendorlib.patch
#include libwhisker1 compatibility bridge
Patch1:         %{real_name}-2.4-lw1bridge.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Net::SSLeay)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::Simple)
# All SSL and network related packages are optional at run time.
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Libwhisker is a Perl library useful for HTTP testing scripts.  It
contains a pure-Perl implementation of functionality found in the LWP,
URI, Digest::MD5, Digest::MD4, Data::Dumper, Authen::NTLM, HTML::Parser,
HTML::FormParser, CGI::Upload, MIME::Base64, and GetOpt::Std modules.
Libwhisker is designed to be portable (a single perl file), fast (general
benchmarks show libwhisker is faster than LWP), and flexible (great care
was taken to ensure the library does exactly what you want to do, even
if it means breaking the protocol).

%package doc
Summary:        Development documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Examples how to use LW(2) Perl module.


%prep
%setup -qn %{real_name}-%{version}
%patch0 -p1
%patch1 -p1
mv compat/{lw,LW}.pm
# Fix EOLs
for F in CHANGES KNOWNBUGS LICENSE README docs/* scripts/*; do
    sed -e 's/\r$//' "$F" > "${F}.new"
    touch -r "$F"{,.new}
    mv "$F"{.new,}
done
# Fix interpreter path
for F in scripts/*.pl; do
    sed -e '1 s|^#!perl|#!/usr/bin/perl|' "$F" > "${F}.new"
    chmod a+x "${F}.new"
    touch -r "$F"{,.new}
    mv "$F"{.new,}
done


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
# Create directories, not created by Makefile.pl
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3

make install DESTDIR=$RPM_BUILD_ROOT

# Install documentation
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a docs scripts $RPM_BUILD_ROOT%{_datadir}/%{name}

#fix permissions
chmod 0644 $RPM_BUILD_ROOT/%{perl_vendorlib}/*

%check
cd t 
perl ./test.pl

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES KNOWNBUGS LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man?/*

%files doc
%defattr(-,root,root,-)
%{_datadir}/%{name}


%changelog
* Wed Aug 11 2010 Petr Pisar <ppisar@redhat.com> - 2.5-1
- 2.5 bump
- License changed from to 2-clause-BSD
- Remove optional Requires.
- Enable tests
- Distribute developer examples in `doc' subpackage

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
