Name: tuxerjoch
Summary: Very simple weblog software.
Version: 31
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

cp -Rvf ./bin/*               %{buildroot}/usr/local/lib/%{name}/
cp -vf ./README.md            %{buildroot}/usr/local/lib/%{name}/
cp -vf ./LICENSE              %{buildroot}/usr/local/lib/%{name}/
mv -f %{buildroot}/usr/local/lib/%{name}/%{name}.conf  %{buildroot}/usr/local/lib/%{name}/%{name}.conf.sample
#cp -v ./tuxerjoch.service    %{buildroot}/usr/lib/systemd/system/tuxerjoch.service
cd ..
rm -Rvf ./tuxerjoch-master


%post
if [ $1 -eq 1 ]; then
    echo "First install"
else
    echo "Upgrade"
fi
useradd tuxerjoch

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
%config
#/usr/lib/systemd/system/tuxerjoch.service
# %dir  /usr/share/doc/olaf-system-post-init/



%changelog
* Wed Aug 12 2015 briefkasten@olaf-radicke.de - 31.1
- Change url forme and added date in article url now.
* Sat Aug  8 2015 briefkasten@olaf-radicke.de - 30.1
- Small bugfix in site title.
* Thu Aug  6 2015 briefkasten@olaf-radicke.de - 29.1
- Add a draft mode for the articles.
* Wed Aug  5 2015 briefkasten@olaf-radicke.de - 28.1
- Add a update function for designs.
* Sat Aug  1 2015 briefkasten@olaf-radicke.de - 27.1
- Bugfix in article list: Remove html filter. Using force flag by install.
* Tue Jul 28 2015 briefkasten@olaf-radicke.de - 26.1
- Bugfix in file reading operation.
* Tue Jul 28 2015 briefkasten@olaf-radicke.de - 25.1
- Include bugfix.
* Tue Jul 28 2015 briefkasten@olaf-radicke.de - 24.1
- Bugfix in url route.
* Tue Jul 28 2015 briefkasten@olaf-radicke.de - 23.1
- Ingratiate html statistic output from the goaccess tool.
* Sat Jul 25 2015 briefkasten@olaf-radicke.de - 22.1
- Show now create date or update date or all together in Artikel.
* Sat Jul 25 2015 briefkasten@olaf-radicke.de - 21.1
- Add a file manager.
* Wed Jul 22  2015 briefkasten@olaf-radicke.de - 20.1
- Add about site.
* Wed Jul 22  2015 briefkasten@olaf-radicke.de - 19.1
- Fixes in rss feed function.
* Wed Jul 22  2015 briefkasten@olaf-radicke.de - 18.1
- Some fixes in rss feed function.
* Wed Jul 22  2015 briefkasten@olaf-radicke.de - 17.1
- Add rss feed function.
* Wed Jul 22  2015 briefkasten@olaf-radicke.de - 16.1
- Rename uri path of atom feed.
* Tue Jul 21  2015 briefkasten@olaf-radicke.de - 15.1
- Set mime typ of atom feed.
* Tue Jul 21  2015 briefkasten@olaf-radicke.de - 13.1
- Remove sytemd configuration from spec.
* Fri Jul 17  2015 briefkasten@olaf-radicke.de - 12.1
- Remove English in the footer line.
* Thu Jul 16  2015 briefkasten@olaf-radicke.de - 11.1
- Bugfix: program generating a empty tag_statistics document, if there not exist.
* Thu Jul 16  2015 briefkasten@olaf-radicke.de - 10.1
- Bugfix in tag page.
* Thu Jul 16  2015 briefkasten@olaf-radicke.de - 9.1
- Markiere die Systemd-Config als Konfiguration.
* Tue Jul 14  2015 briefkasten@olaf-radicke.de - 8.1
- Fixing: local variable response_data referenced before assignment.
* Tue Jul 14  2015 briefkasten@olaf-radicke.de - 7.1
- Fehlermeldung bei fehlender Tag-Liste korrigiert.
* Tue Jul 14  2015 briefkasten@olaf-radicke.de - 6.1
- Die ausgeliferte Konfiguration bekommt die Ändung sample.
* Tue Jul 14  2015 briefkasten@olaf-radicke.de - 5.1
- Systemd hat probleme wenn tuxerjoch nicht unter Benutzer root läuft.
* Sun Jul 12 2015 briefkasten@olaf-radicke.de - 3.1
- System user für den Service hinzugefügt.
* Sun Jul 12 2015 briefkasten@olaf-radicke.de - 1.1
- Init-Version.

