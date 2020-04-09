package main

const Version = "0.2.5"

var GitCommit string

func buildVersion() string {
	version := Version
	if GitCommit != "" {
		version += " - " + GitCommit
	}
	return version
}
