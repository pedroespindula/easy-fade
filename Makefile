.PHONY: install
SITE_PACKAGES := $(shell pip3.6 show pip | grep '^Location' | cut -f2 -d':')

$(SITE_PACKAGES): requirements.txt; \
    pip3.6 install -r requirements.txt --user;
