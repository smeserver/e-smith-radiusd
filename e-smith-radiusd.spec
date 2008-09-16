Summary: e-smith server and gateway - configure PPTP inbound VPN
%define name e-smith-radiusd
Name: %{name}
%define version 1.0.0
%define release 18
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Patch0: e-smith-radiusd-1.0.0-2.mitel_patch
Patch1: e-smith-radiusd-1.0.0-3.mitel_patch
Patch2: e-smith-radiusd-1.0.0-4.mitel_patch
Patch3: e-smith-radiusd-1.0.0-5.mitel_patch
Patch4: e-smith-radiusd-1.0.0-6.mitel_patch
Patch5: e-smith-radiusd-1.0.0-7.mitel_patch
Patch6: e-smith-radiusd-1.0.0-9.mitel_patch
Patch7: e-smith-radiusd-1.0.0-11.mitel_patch
Patch8: e-smith-radiusd-1.0.0-TemplateSplit.patch
Patch9: e-smith-radiusd-1.0.0-clients.conf_perms.patch
Patch10: e-smith-radiusd-1.0.0-servers_perm.patch
Patch11: e-smith-radiusd-1.0.0-FixedIp.patch 
Patch12: e-smith-radiusd-1.0.0-allowForMoreAuthModules.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: e-smith-base >= 4.13.16-27
Requires: e-smith-lib >= 1.15.1-16
Requires: freeradius >= 1.0.1
Requires: radiusclient >= 0.3.2
BuildRequires: e-smith-devtools >= 1.13.1-03
BuildArchitectures: noarch
%define stunnelid 451

%description
e-smith server and gateway - configure radius server

%changelog
* Wed Aug 20 2008 Jonathan Martens <smeserver-contribs@snetram.nl> 1.0.0-18
- Allow for multiple auth modules in radiusd.conf [SME: 4166]

* Sat Aug 09 2008 Gavin Weight <gweight@gmail.com> 1.0.0-17
- Remove the Requires kernel =>2.4 line. [SME: 4483]

* Fri May 18 2007 Federico Simoncelli <federico.simoncelli@gmail.com> 1.0.0-16
- Added support for fixed ip addresses in the pptp vpn [SME: 1230]

* Sun Apr 29 2007 Shad L. Lords <slords@mail.com>
- Clean up spec so package can be built by koji/plague

* Fri Apr 06 2007 Shad L. Lords <slords@mail.com> 1.0.0-14
- Fix perms on servers file [SME: 2720]

* Fri Apr 06 2007 Shad L. Lords <slords@mail.com> 1.0.0-14
- Fix perms on client.conf file [SME: 2708]

* Wed Mar 07 2007 Shad L. Lords <slords@mail.com> 1.0.0-13
- Break up auth template to allow customization [SME: 2565]

* Thu Dec 07 2006 Shad L. Lords <slords@mail.com>
- Update to new release naming.  No functional changes.
- Make Packager generic

* Wed Nov 30 2005 Gordon Rowell <gordonr@gormand.com.au> 1.0.0-12
- Bump release number only

* Tue Sep 27 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-11]
- Fix run script so that output actually goes to the logger. [SF: 1280982]

* Mon Sep 26 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-10]
- Make sure that the log/run script is executable, and that
  the log directory exists. [SF: 1280982]
- Make sure that stunnel user exists, by making sure that
  %pre script works :-) (%stunnelid was not defined).

* Mon Sep 26 2005 Gordon Rowell <gordonr@e-smith.com>
- [1.0.0-9]
- Add a log/run script [SF: 1280982]

* Fri Sep  2 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-8]
- Make sure that stunnel user exists, by %pre script.

* Mon Jul 18 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-7]
- [More updates from Shad.]
- Add accounting into radiusd
- Let radius do its own normal logging

* Tue Jul 12 2005 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-6]
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
perl createlinks
# Manage supervise and multilog.
mkdir -p root/service
ln -s ../var/service/radiusd root/service/radiusd
mkdir -p root/var/service/radiusd/supervise
touch root/var/service/radiusd/down
mkdir -p root/var/log/radiusd

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    --dir /var/service/radiusd 'attr(01755,root,root)' \
    --file /var/service/radiusd/down 'attr(0644,root,root)' \
    --file /var/service/radiusd/run 'attr(0755,root,root)' \
    --file /var/service/radiusd/log/run 'attr(0755,root,root)' \
    --dir /var/service/radiusd/supervise 'attr(0700,root,root)' \
    --dir /var/log/radiusd 'attr(0755,smelog,smelog)' \
    > %{name}-%{version}-%{release}-filelist
echo "%doc COPYING" >> %{name}-%{version}-%{release}-filelist

%postun

%pre
/sbin/e-smith/create-system-user stunnel %{stunnelid} \
    'chrooted stunnel user user' /var/log/imap/ssl /bin/false

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
