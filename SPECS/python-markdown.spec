%if 0%{?fedora} || 0%{?rhel} >= 7
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

%global srcname Markdown
%global pkgname markdown

Name:           python-%{pkgname}
Version:        2.6.11
Release:        2%{?dist}
Summary:        Markdown implementation in Python
License:        BSD
URL:            https://python-markdown.github.io/
Source0:        https://files.pythonhosted.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch


%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%if %{with python2}
%package -n python2-%{pkgname}
Summary:        Markdown implementation in Python
BuildRequires:  python2-devel
BuildRequires:  python2-nose
%if ! 0%{?rhel}
BuildRequires:  python2-yaml
%else
BuildRequires:  python-yaml
%endif
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.
%endif # with python2


%if %{with python3}
%package -n python%{python3_pkgversion}-%{pkgname}
Summary:        Markdown implementation in Python
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-PyYAML
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}

%description -n python%{python3_pkgversion}-%{pkgname}
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.
%endif # with python3


%prep
%setup -qc -n %{srcname}-%{version}
%if %{with python2}
cp -a %{srcname}-%{version} python2
%endif # with python2

%if %{with python3}
cp -a %{srcname}-%{version} python3
%endif # with python3


%build
%if %{with python2}
pushd python2
%py2_build
popd
%endif # with python2

%if %{with python3}
pushd python3
%py3_build
popd
%endif # with python3


%install
%if %{with python2}
pushd python2
%py2_install

# rename binary
mv %{buildroot}%{_bindir}/markdown_py{,-%{python2_version}}
ln -s markdown_py-%{python2_version} %{buildroot}%{_bindir}/markdown_py-2

# process license file
PYTHONPATH=%{buildroot}%{python2_sitelib} \
  %{buildroot}%{_bindir}/markdown_py-%{python2_version} \
  LICENSE.md > LICENSE.html
popd
%endif # with python2

%if %{with python3}
pushd python3
%py3_install

# rename binary
mv %{buildroot}%{_bindir}/markdown_py{,-%{python3_version}}
ln -s markdown_py-%{python3_version} %{buildroot}%{_bindir}/markdown_py-3

# process license file
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/markdown_py-%{python3_version} \
  LICENSE.md > LICENSE.html
popd
%endif # with python3

%if %{without python3}
ln -s markdown_py-%{python2_version} %{buildroot}%{_bindir}/markdown_py
%else
ln -s markdown_py-%{python3_version} %{buildroot}%{_bindir}/markdown_py
%endif # without python3


%check
%if %{with python2}
pushd python2
%{__python2} run-tests.py
popd
%endif # with python2

%if %{with python3}
pushd python3
%{__python3} run-tests.py
popd
%endif # with python3


%if %{with python2}
%files -n python2-%{pkgname}
# temporarily skip packaging docs - see also
# https://github.com/Python-Markdown/markdown/issues/621
#doc python2/build/docs/*
%license python2/LICENSE.*
%{python2_sitelib}/*
%if %{without python3}
%{_bindir}/markdown_py
%endif # without python3
%{_bindir}/markdown_py-2
%{_bindir}/markdown_py-%{python2_version}
%endif # with python2


%if %{with python3}
%files -n python%{python3_pkgversion}-%{pkgname}
# temporarily skip packaging docs - see also
# https://github.com/Python-Markdown/markdown/issues/621
#doc python3/build/docs/*
%license python3/LICENSE.*
%{python3_sitelib}/*
%{_bindir}/markdown_py
%{_bindir}/markdown_py-3
%{_bindir}/markdown_py-%{python3_version}
%endif # with python3


%changelog
* Thu Jun 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.6.11-2
- Conditionalize the python2 subpackage

* Sun Feb 11 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.11-1
- Update to 2.6.11.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.9-2
- Fix BRs.

* Wed Aug 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.9-1
- Update to 2.6.9.
- Allow building a python3 subpackage on EPEL7+.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.8-1
- Update to 2.6.8.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.6.7-2
- Rebuild for Python 3.6

* Sat Sep 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.7-1
- Update to 2.6.7.
- Update Source0 URL.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr  5 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.6-1
- Update to 2.6.6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 29 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.5-1
- Update to 2.6.5.

* Sat Nov 21 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.4-1
- Update to 2.6.4.
- Follow updated Python packaging guidelines.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.2-1
- Update to 2.6.2.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-2
- Add license file.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.
- Apply updated Python packaging guidelines.

* Sun Feb 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6-1
- Update to 2.6.
- Update the upstream URL.

* Sun Nov 23 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Thu Oct  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.1-1
- Update to 2.5.1.

* Thu Sep 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5-1
- Update to 2.5.
- Add BR on PyYAML.

* Wed Jun  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.1-1
- Update to 2.4.1.

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 15 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4-1
- Update to 2.4.
- Update Python3 conditional.
- Fix wrong line endings.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Thomas Moschny <thomas.moschny@gmx.dee> - 2.3.1-2
- Move python3 runtime dependency to python3 subpackage (rhbz#986376).

* Mon Apr  8 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.

* Mon Mar 18 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3-1
- Update to 2.3.
- Spec file cleanups.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.
- Update url.
- Add patch from upstream git for failing test.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.
- Fix rhel conditional.
- Binary has been renamed.
- Build python3 subpackage.
- Include documentation in HTML instead of Markdown format.
- Run tests.

* Wed Sep 07 2011 Jesse Keating <jkeating@redhat.com> - 2.0.3-4
- Set a version in the rhel macro

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct  8 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-3
- Add requirement on python-elementtree, which was a separate package
  before Python 2.5.
- Re-add changelog entries accidentally removed earlier.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Upstream stripped .py of the cmdline script.

* Sat Apr 25 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Update to 2.0.
- Adjusted source URL.
- License changed to BSD only.
- Upstream now provides a script to run markdown from the cmdline.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7-2
- Rebuild for Python 2.6

* Mon Aug  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.7-1
- New package.
