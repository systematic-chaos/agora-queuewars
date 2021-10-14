.PHONY: gnats gnatsd_remove release clean
COMMIT_ID=$(shell git log --pretty=format:'%h' -n 1)
OUT=build
PKG=$(OUT)/agora-$(COMMIT_ID).tar.gz
PKG_SOLVED=$(OUT)/agora-solved-$(COMMIT_ID).tar.gz

release: clean $(PKG) $(PKG_SOLVED)

gnatsd: gnatsd_remove
	docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name gnatsd -ti nats:latest

gnatsd_remove:
	-docker rm gnatsd

clean:
	rm -rf $(OUT)

$(OUT):
	mkdir -p $(OUT)

$(PKG): $(OUT)
	git archive --worktree-attributes --format=tar HEAD . | gzip -9 > $(PKG)

$(PKG_SOLVED): $(PKG)
	git archive --format=tar HEAD . | gzip -9 > $(PKG_SOLVED)
