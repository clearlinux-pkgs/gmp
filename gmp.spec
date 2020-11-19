Name:           gmp
Version:        6.2.1
Release:        42
License:        LGPL-3.0 GPL-3.0
Summary:        GNU multiprecision arithmetic library
Url:            http://gmplib.org/
Group:          devel
Source0:        https://mirrors.kernel.org/gnu/gmp/gmp-6.2.1.tar.xz
BuildRequires:  grep bison flex readline-dev  ncurses-dev zlib-dev32 readline-dev32
BuildRequires:  libstdc++-dev
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  glibc-dev32
BuildRequires:  glibc-libc32


%description
GNU multiprecision arithmetic library.

%package gmpxx
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel

%description gmpxx
GNU multiprecision arithmetic library.


%package dev
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel
Requires:       gmp-lib 
Requires:       gmp-gmpxx

%description  dev
GNU multiprecision arithmetic library.

%package dev32
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel
Requires:       gmp-lib 
Requires:       gmp-dev
Requires:	gmp-gmpxx

%description  dev32
GNU multiprecision arithmetic library.

%package doc
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          doc

%description  doc
GNU multiprecision arithmetic library.

%package lib
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel

%description lib
GNU multiprecision arithmetic library.

%package lib-hsw
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel
Requires:	gmp-lib

%description lib-hsw
GNU multiprecision arithmetic library.

%package lib32
License:        LGPL-3.0 and GPL-3.0
Summary:        GNU multiprecision arithmetic library
Group:          devel

%description lib32
GNU multiprecision arithmetic library.

%prep
%setup -q
pushd ..
cp -a gmp-%{version} build32
cp -a gmp-%{version} buildhsw
popd

%build
# gmp fails to compile with PIE
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="-O3  -g -fno-semantic-interposition -flto=4"
export CXXFLAGS="$CFLAGS"

./configure --host=%{_arch}-unknown-linux-gnu --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/bin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/usr/com --mandir=/usr/share/man --infodir=/usr/share/info --enable-cxx=detect --disable-static --enable-shared

make %{?_smp_mflags}
make check ||:

pushd ../buildhsw
export CFLAGS="-O3  -g -fno-semantic-interposition -march=haswell -ffat-lto-objects  -flto=4 "
export CXXFLAGS="$CFLAGS"

./configure --host=coreihwl-unknown-linux-gnu --build=coreihwl-linux-gnu --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/bin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64/haswell --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --enable-cxx=detect --disable-static --enable-shared
make %{?_smp_mflags}
popd
pushd ../build32
export CFLAGS="-O3  -g -fno-semantic-interposition -m32 -mstackrealign"
export CXXFLAGS="$CFLAGS"

./configure --host=i686-unknown-linux-gnu --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/bin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib32 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/usr/share --mandir=/usr/share/man --infodir=/usr/share/info --enable-cxx=detect --disable-static --enable-shared
make %{?_smp_mflags}

popd


%install
pushd ../build32
%make_install32
popd
pushd ../buildhsw
%make_install
popd
%make_install

# Fix hardcoded size of mp_limb_t (long) with GCC predefined macros
sed -i '/#define GMP_LIMB_BITS/s/64/(__SIZEOF_LONG__ * __CHAR_BIT__)/' %{?buildroot}/usr/include/gmp.h

%files

%files gmpxx
%{_libdir}/libgmpxx.so.4
%{_libdir}/libgmpxx.so.4.*

%files dev
%{_includedir}/gmp.h
%{_includedir}/gmpxx.h
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
/usr/lib64/pkgconfig/gmp.pc
/usr/lib64/pkgconfig/gmpxx.pc


%files doc
%{_infodir}/gmp.info
%{_infodir}/gmp.info-2
%{_infodir}/gmp.info-1

%files lib
%{_libdir}/libgmp.so.10
%{_libdir}/libgmp.so.10.*


%files lib32
/usr/lib32/libgmp.so.10
/usr/lib32/libgmp.so.10.*
/usr/lib32/libgmpxx.so.4
/usr/lib32/libgmpxx.so.4.*

%files dev32
/usr/lib32/libgmpxx.so
/usr/lib32/libgmp.so
/usr/lib32/pkgconfig/gmp.pc
/usr/lib32/pkgconfig/gmpxx.pc


%files lib-hsw
%exclude /usr/lib64/haswell/libgmp.so
/usr/lib64/haswell/libgmp.so.10
/usr/lib64/haswell/libgmp.so.10.*
