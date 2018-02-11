# AWS role switcher for Alfred

This is a basic utility to make it easier to switch roles in AWS.

It is currently based on my own AWS config file, so milage may vary.

This should be considered a work in progress.

It will read `Profiles` from `~/.aws/config`, expecting them to be in the format:

    [profile Thing]
    role_arn = arn:partition:service:region:account-id:resourcetype/DisplayName
