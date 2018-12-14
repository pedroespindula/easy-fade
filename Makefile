.PHONY: install
SITE_PACKAGES := $(shell pip3 show pip | grep '^Location' | cut -f2 -d':')

$(SITE_PACKAGES): requirements.txt; \
    pip3 install -r requirements.txt --user;
