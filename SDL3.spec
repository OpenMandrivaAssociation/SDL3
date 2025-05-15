# SDL2 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define dev32name %mklib32name %{name} -d

%global optflags %{optflags} -O3 -I%{_includedir}/libunwind

Summary:	Simple DirectMedia Layer
Name:		SDL3
Version:	3.2.14
Release:	1
License:	Zlib
Group:		System/Libraries
Url:		https://www.libsdl.org/
Source0:	https://github.com/libsdl-org/SDL/releases/download/%{version}/SDL3-%{version}.tar.gz
#Patch1:		SDL2-2.0.3-cmake-joystick.patch
%ifnarch %{riscv}
BuildRequires:	nas-devel
%endif
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libdecor-0)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(libunwind-generic)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libpulse-simple)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(samplerate)
%ifnarch %{arm}
BuildRequires:	vulkan-devel
%endif
BuildRequires:	cmake
BuildRequires:	ninja
%if %{with compat32}
BuildRequires:	devel(libasound)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libGLU)
BuildRequires:	devel(libdrm)
BuildRequires:	devel(libpulse)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libXcursor)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXinerama)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libXss)
BuildRequires:	devel(libXxf86vm)
BuildRequires:	devel(libz)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libpulse-simple)
BuildRequires:	devel(libEGL)
BuildRequires:	devel(libgbm)
BuildRequires:	devel(libxkbcommon)
BuildRequires:	devel(libsamplerate)
BuildRequires:	libunwind-nongnu-devel
%endif

#----------------------------------------------------------------------------

%description
This is the Simple DirectMedia Layer, a generic API that provides low level
access to audio, keyboard, mouse, and display framebuffer across multiple
platforms.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%files -n %{libname}
%license %{_datadir}/licenses/SDL3
%{_libdir}/libSDL3.so.0*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	pkgconfig(alsa)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(egl)

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%files -n %{devname}
%doc BUGS.txt WhatsNew.txt
%{_libdir}/pkgconfig/sdl3.pc
%{_libdir}/libSDL3.so
%{_libdir}/libSDL3_test.a
%dir %{_includedir}/SDL3
%{_includedir}/SDL3/*.h
%{_libdir}/cmake/SDL3/*

#----------------------------------------------------------------------------

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for %{name} (32-bit)
Group:		System/Libraries

%description -n	%{lib32name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%files -n %{lib32name}
%{_prefix}/lib/libSDL3.so.0*

#----------------------------------------------------------------------------

%package -n %{dev32name}
Summary:	Headers for developing programs that will use %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	devel(libasound)
Requires:	devel(libGL)
Requires:	devel(libGLU)
Requires:	devel(libEGL)

%description -n %{dev32name}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/sdl3.pc
%{_prefix}/lib/libSDL3.so
%{_prefix}/lib/libSDL3_test.a
%{_prefix}/lib/cmake/SDL3/*
%endif

%prep
%autosetup -p1

%if %{with compat32}
%cmake32 \
	-DSSEMATH:BOOL=ON \
	-DESD:BOOL=OFF \
	-DESD_SHARED:BOOL=OFF \
	-DSDL_STATIC:BOOL=OFF \
	-DVIDEO_VULKAN:BOOL=ON \
	-DRPATH:BOOL=OFF \
	-G Ninja
cd ..
%endif

%cmake \
%ifnarch %{ix86} %{x86_64}
	-DSSEMATH:BOOL=OFF \
%endif
%ifarch znver1
	-DSSEMATH:BOOL=ON \
%endif
	-DESD:BOOL=OFF \
	-DESD_SHARED:BOOL=OFF \
	-DSDL_STATIC:BOOL=OFF \
	-DVIDEO_VULKAN:BOOL=ON \
	-DRPATH:BOOL=OFF \
	-DLIB_SUFFIX="" \
	-G Ninja

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
