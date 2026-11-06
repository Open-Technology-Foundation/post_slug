# post_slug - C port Makefile (BCS1212 compliant)
# Version: 1.1.0

# Required BCS1212 variables
PREFIX     ?= /usr/local
BINDIR     ?= $(PREFIX)/bin
LIBDIR     ?= $(PREFIX)/lib
INCLUDEDIR ?= $(PREFIX)/include
MANDIR     ?= $(PREFIX)/share/man/man1
COMPDIR    ?= /etc/bash_completion.d
DESTDIR    ?=

# Compiler flags
CC      ?= cc
CFLAGS  ?= -O2 -std=c11 -Wall -Wextra -Wpedantic
AR      ?= ar

# Directory of this Makefile (trailing slash). Anchors source paths so
# 'make install' works regardless of invoking CWD.
srcdir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all build install uninstall check test help clean

# BCS1212: 'all' aliases 'help', never 'install' — accidental `make` must
# never modify the system.
all: help

# 'build' produces local artefacts (not BCS-required; needed for a C project).
build: _post_slug libpost_slug.a

_post_slug: $(srcdir)post_slug.c $(srcdir)post_slug.h
	$(CC) $(CFLAGS) -o $@ $(srcdir)post_slug.c

post_slug.o: $(srcdir)post_slug.c $(srcdir)post_slug.h
	$(CC) $(CFLAGS) -DPOST_SLUG_LIB_ONLY -c -o $@ $(srcdir)post_slug.c

libpost_slug.a: post_slug.o
	$(AR) rcs $@ $<

install: build
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 _post_slug $(DESTDIR)$(BINDIR)/post_slug
	install -d $(DESTDIR)$(LIBDIR)
	install -m 644 libpost_slug.a $(DESTDIR)$(LIBDIR)/libpost_slug.a
	install -d $(DESTDIR)$(INCLUDEDIR)
	install -m 644 $(srcdir)post_slug.h $(DESTDIR)$(INCLUDEDIR)/post_slug.h
	@if [ -z "$(DESTDIR)" ]; then $(MAKE) --no-print-directory check; fi

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/post_slug
	rm -f $(DESTDIR)$(LIBDIR)/libpost_slug.a
	rm -f $(DESTDIR)$(INCLUDEDIR)/post_slug.h

check:
	@command -v post_slug >/dev/null 2>&1 \
	  && echo 'post_slug: OK' \
	  || echo 'post_slug: NOT FOUND (check PATH)'

# Cross-language validation; small dataset for fast turnaround. The
# validator runs this directory's _post_slug itself.
test: build
	cd $(srcdir)../unittests && ./validate_slug_scripts -q datasets/edge_cases.txt

clean:
	rm -f _post_slug post_slug.o libpost_slug.a

help:
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@echo '  build       Build _post_slug binary and libpost_slug.a'
	@echo '  install     Install binary, library, header to $(PREFIX)'
	@echo '  uninstall   Remove installed files'
	@echo '  check       Verify installation (post_slug in PATH)'
	@echo '  test        Run cross-language validation on edge_cases dataset'
	@echo '  clean       Remove build artefacts'
	@echo '  help        Show this message'
	@echo ''
	@echo 'Variables:'
	@echo '  PREFIX      Installation prefix      (default: /usr/local)'
	@echo '  BINDIR      Binary install dir       (default: $$PREFIX/bin)'
	@echo '  LIBDIR      Library install dir      (default: $$PREFIX/lib)'
	@echo '  INCLUDEDIR  Header install dir       (default: $$PREFIX/include)'
	@echo '  DESTDIR     Staged install root      (for packaging)'
	@echo '  CC          C compiler               (default: cc)'
	@echo '  CFLAGS      C compiler flags         (default: -O2 -std=c11 -Wall -Wextra -Wpedantic)'

#fin
