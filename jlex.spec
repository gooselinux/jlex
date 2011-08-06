# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section free

Name:           jlex
Version:        1.2.6
Release:        9.5%{?dist}
Epoch:          0
Summary:        A Lexical Analyzer Generator for Java
License:        BSD
Group:          Development/Libraries
Source0:        http://www.cs.princeton.edu/~appel/modern/java/JLex/Archive/%{version}/Main.java
Source1:        %{name}-%{version}.build.xml
Patch0:         %{name}-%{version}.static.patch
URL:            http://www.cs.princeton.edu/~appel/modern/java/JLex/
BuildRequires:  ant, sed, jpackage-utils > 1.4
%if ! %{gcj_support}
BuildArch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
JLex is a Lexical Analyzer Generator for Java

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -T
cp %{SOURCE0} .
%patch0 -p0
cp %{SOURCE1} build.xml

%build
unset CLASSPATH
ant

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%{_javadir}

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jlex-1.2.6.jar.*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.2.6-9.5
- Fix Group tags
- Remove ghost symlinking in %%post{,un}
- Add cleaning of buildroot in %%install
- Remove dot in javadoc Summary
- Fix URL for Source0
- Fix mixed tabs and spaces

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.2.6-9.4
- Rebuilt for RHEL 6

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0:1.2.6-9.3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.6-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.6-7.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.6-6.3
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.6-6jpp.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.6-6jpp.1
- Autorebuild for GCC 4.3

* Fri Aug 04 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.6-5jpp.1
- Re-sync with latest JPP version.
- Use new naming convention.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.2.6-4jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.6-4jpp_1fc
- Conditional native compilation for GCJ.
- Remove clean up of build root in prep section.

* Tue Jul 18 2006 Fernando Nasser <fnasser@redhat.com> - 1.2.6-3jpp
- First JPP 1.7 build

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.2.6-1jpp_4fc
- rebuild

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 1.2.6-1jpp_3fc
- rebuilt again

* Tue Dec 13 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 1.2.6-1jpp_2fc
- Build into Fedora.

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 1.2.6-2jpp
- Rebuild with ant-1.6.2

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 1.2.6-1jpp_1rh
- RH vacuuming

* Wed Mar 26 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org > 1.2.6-1jpp
- for jpackage-utils 1.5

* Tue Aug 20 2002 Ville Skyttä <ville.skytta@iki.fi> 1.2.5-5jpp
- Use the Xalan/XSLTC version (backwards-compatible with the official one).
- Renamed jar to jlex.jar (was JLex.jar).
- Some spec cleanup.

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2.5-4jpp
- fixed source perls

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2.5-3jpp
- renamed to %%{name}
- section macro
- bzipped additional sources

* Wed Jun 26 2002 Henri Gomez <hgomez@slib.fr> 1.2.5-2jpp
- removed JLex build dir

* Wed Jun 26 2002 Henri Gomez <hgomez@slib.fr> 1.2.5-1jpp
- first JPackage release
