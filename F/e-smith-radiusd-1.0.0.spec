Summary: e-smith server and gateway - configure PPTP inbound VPN
%define name e-smith-radiusd
Name: %{name}
%define version 1.0.0
%define release 5sme01
Version: %{version}
Release: %{release}
License: GPL
Group: Networking/Daemons
Packager: e-smith developers <bugs@e-smith.com>
Source: %{name}-%{version}.tar.gz
Patch0: e-smith-radiusd-1.0.0-2.mitel_patch
Patch1: e-smith-radiusd-1.0.0-3.mitel_patch
Patch2: e-smith-radiusd-1.0.0-4.mitel_patch
Patch3: e-smith-radiusd-1.0.0-5.mitel_patch
Patch4: e-smith-radiusd-1.0.0-5sme01.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: e-smith-base >= 4.13.16-27
Requires: kernel => 2.4
Requires: e-smith-lib >= 1.15.1-16
Requires: freeradius >= 1.0.1
Requires: radiusclient >= 0.3.2
BuildRequires: e-smith-devtools >= 1.13.1-03
BuildArchitectures: noarch

%description
e-smith server and gateway - configure radius server

%changelog
* Sun Jul 03 2005 Shad L. Lords <slords@mail.com>
- [1.0.0-5sme01]
- Expand /etc/raddb/users in user-lock [SF: 1225995]
- Expand sigterm in password-modify, ldap-update [SF: 1225995]

* Fri Jun 24 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-5]
- Expand /etc/raddb/users in password-modify event [SF: 1215401]

* Fri Jun 24 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-4]
- Add missing patch to allow local hosts to be radius clients. [SF: 1215401]

* Thu Jun 16 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-3]
- Use e-smith-services startup symlink for radiusd, so that 'status'
  property is honoured. [SF: 1215401]

* Tue Jun 14 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-2]
- Patches from Shad to automate radiusd startup, and to allow local hosts to
  be radius clients. [SF: 1215401]

* Mon Jun 13 2005 Shad L. Lords <slords@mail.com>
- [1.0.0-1]
- initial

%prep
%setup
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
perl createlinks
# Manage supervise and multilog.
mkdir -p root/service
ln -s ../var/service/radiusd root/service/radiusd
mkdir -p root/var/service/radiusd/supervise
touch root/var/service/radiusd/down
mkdir -p root/var/service/radiusd/log/supervise
mkdir -p root/var/log/radiusd

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    --dir /var/service/radiusd 'attr(01755,root,root)' \
    --file /var/service/radiusd/down 'attr(0644,root,root)' \
    --file /var/service/radiusd/run 'attr(0755,root,root)' \
    --dir /var/service/radiusd/log 'attr(0755,root,root)' \
    --dir /var/service/radiusd/log/supervise 'attr(0700,root,root)' \
    --dir /var/service/radiusd/supervise 'attr(0700,root,root)' \
    --file /var/service/radiusd/log/run 'attr(0755,root,root)' \
    --dir /var/log/radiusd 'attr(2750,smelog,smelog)' \
    > %{name}-%{version}-%{release}-filelist
echo "%doc COPYING" >> %{name}-%{version}-%{release}-filelist

%postun

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
