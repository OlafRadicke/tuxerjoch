Name: tuxerjoch
Summary: Very simple weblog software.
Version: 1
Group: web
License: AGPL
Release: 1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
URL: https://github.com/OlafRadicke/tuxerjoch
BuildArch: noarch
BuildRequires: unzip, wget
Requires: python3, python3-requests, python3-bottle, python3-simplejson, python3-cherrypy


%description
Verry simple weblog. Based on bottle and CouchDB.

#%prep

%build

%install
if [ $1 -eq 1 ]; then
    echo "First install"
else
    echo "Upgrade"
fi

wget https://github.com/OlafRadicke/tuxerjoch/archive/master.zip
unzip -u master.zip
ls -lah
cd tuxerjoch-master
ls -lah

mkdir -p %{buildroot}/usr/local/lib/%{name}
cp -Rv ./bin/* %{buildroot}/usr/local/lib/%{name}/
cp -Rv ./README.md %{buildroot}/usr/local/lib/%{name}/
cp -Rv ./LICENSE %{buildroot}/usr/local/lib/%{name}/

cd ..
rm -Rvf ./tuxerjoch-master


%post


%clean
# rm -Rvf /tmp/master.zip /tmp/cxxtools-master
#rm -fr $RPM_BUILD_ROOT

%postun




%files
/usr/local/lib/%{name}/
# %dir  /usr/share/doc/olaf-system-post-init/



%changelog
* Sun Jul 12 2015 briefkasten@olaf-radicke.de - 1
- Init-Version.

