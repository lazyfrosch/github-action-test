PROJECT = github-action-test

GIT_COMMIT = $(shell git rev-list -1 HEAD)
GO_BUILD = go build -v -ldflags "-X main.GitCommit=$(GIT_COMMIT)"

.PHONY: all clean build test

all: build test

distclean: clean
clean:
	rm -rf build/

build:
	GOOS=linux GOARCH=amd64 $(GO_BUILD) -o build/$(PROJECT)-amd64 .
	GOOS=linux GOARCH=386 $(GO_BUILD) -o build/$(PROJECT)-i386 .

test:
	go test -v ./...

release:
	@test -n "$(VERSION)" || (echo "Please specify version like so: make release VERSION=1.0.1"; false)
	@echo Preparing release for version $(VERSION)
	git log --use-mailmap | grep ^Author: | cut -f2- -d' ' | sort | uniq > AUTHORS
	sed -i 's/const Version =.*/const Version = "$(VERSION)"/' version.go
	github_changelog_generator --future-release "v$(VERSION)"
	git add AUTHORS CHANGELOG.md version.go
	git diff --cached
	git status
	@echo
	@read -p "Want me to commit changes for version $(VERSION)? [y/N] " question; case "$$question" in y|Y) true ;; *) false;; esac
	git commit -vm "Release version $(VERSION)"
	@echo
	@read -p "Want me to create tag for version $(VERSION)? [y/N] " question; case "$$question" in y|Y) true ;; *) false;; esac
	git tag -s -m "Version $(VERSION)" "v$(VERSION)"
	@echo
	@echo "Please push master and tag to GitHub:"
	@echo "git push origin master v$(VERSION)"
