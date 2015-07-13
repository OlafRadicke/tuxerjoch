Name: tuxerjoch
Summary: Very simple weblog software.
Version: 2
Group: web
License: AGPL
Release: 1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
URL: https://github.com/OlafRadicke/tuxerjoch
BuildArch: noarch
BuildRequires: unzip, wget
#Requires: python3, python3-requests, python3-bottle, python3-simplejson, python3-cherrypy


%description
Verry simple weblog. Based on bottle and CouchDB.

#%prep

#%build

%install

#rm -Rvf %{_builddir}/*
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
mkdir -p %{buildroot}/usr/lib/systemd/system/

cp -Rv ./bin/*               %{buildroot}/usr/local/lib/%{name}/
cp -v ./README.md            %{buildroot}/usr/local/lib/%{name}/
cp -v ./LICENSE              %{buildroot}/usr/local/lib/%{name}/
cp -v ./tuxerjoch.service    %{buildroot}/usr/lib/systemd/system/tuxerjoch.service

cd ..
rm -Rvf ./tuxerjoch-master


%post
systemctl daemon-reload
# systemctl start tuxerjoch.service
# systemctl enable tuxerjoch.service


%clean
# rm -Rvf /tmp/master.zip /tmp/cxxtools-master
#rm -fr $RPM_BUILD_ROOT
rm -Rvf %{_builddir}/*
%postun

%files
/usr/local/lib/%{name}/
/usr/lib/systemd/system/tuxerjoch.service
# %dir  /usr/share/doc/olaf-system-post-init/



%changelog
* Sun Jul 12 2015 briefkasten@olaf-radicke.de - 1
- Init-Version.

