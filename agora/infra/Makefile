IMG_NAME=mbda_fintech

.PHONY: all clean build package

all: clean build package

clean:
	rm -f package.box
	vagrant destroy -f
	rm -rf .vagrant/
	# vagrant box remove $(IMG_NAME)

build:
	vagrant up

package:
	rm -rf .vagrant/machines/default/virtualbox/private_key*
	vagrant package --base $(IMG_NAME)

add:
	vagrant box add $(IMG_NAME) package.box
