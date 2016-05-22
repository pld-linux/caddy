#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests

Summary:	Fast, cross-platform HTTP/2 web server with automatic HTTPS
Name:		caddy
Version:	0.8.3
Release:	0.1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/mholt/caddy/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2d08bf70a7ad4255513bf1e0df174e98
URL:		https://caddyserver.com/
BuildRequires:	golang >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/mholt/%{name}

%description
Caddy is a lightweight, general-purpose web server for Windows, Mac,
Linux, BSD and Android. It is a capable alternative to other popular
and easy to use web servers.

The most notable features are HTTP/2, Let's Encrypt support, Virtual
Hosts, TLS + SNI, and easy configuration with a Caddyfile. In
development, you usually put one Caddyfile with each site. In
production, Caddy serves HTTPS by default and manages all
cryptographic assets for you.

%prep
%setup -q

GOPATH=$(pwd)/vendor
install -d $GOPATH/src/github.com/mholt
ln -s ../../../.. $GOPATH/src/github.com/mholt/caddy

%build
export GOPATH=$(pwd)/vendor

# command extraced by running "build.bash" from git tree
date=$(date -u +"%%a %%b %%d %%H:%%M:%%S %%Z %%Y")
LDFLAGS="\
-X main.buildDate=$date \
-X main.gitTag= \
-X main.gitNearestTag=v%{version} \
-X main.gitCommit= \
-X main.gitShortStat= \
-X main.gitFilesModified= \
"

test -d vendor/src/golang.org || go get ./... || :
%gobuild -o caddy.bin

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p %{name}.bin $RPM_BUILD_ROOT%{_sbindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_sbindir}/%{name}
