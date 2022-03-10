#!python3

"""
This Python 3 script sets the temporary authorization profile "temp" for an IAM user with an MFA device.
This program is known only to work on MacOS, and would require modification for use on Windows or Linux systems.
"""
import subprocess
import json
import configparser
from os.path import expanduser
import os
import sys
import argparse
from re import search


def parse_args():
    """
    Initializes a parser that intakes the CLI arguments when invoking this Python script.
    For usage: python3 temp_auth.py --help
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', type=str, default='default',
                        help='AWS profile to read MFA device serial from')
    parser.add_argument('--serial', type=int, default=None,
                        help='MFA device serial (i.e. arn:aws:iam::<AWS ACCOUNT ID>:mfa/<IAM USER NAME>)')
    parser.add_argument('--token', type=str, default=None,
                        help='MFA token to use for login')
    return parser.parse_args()


def validate_args(args):
    """
    Validates arguments passed in via script invocation. 
    If some arguments are not passed in, check the profile within ~/.aws/credentials.
    If the profile does not exist, allow the user to create the profile.
    """
    config = configparser.ConfigParser()
    config.read(expanduser("~/.aws/credentials"))

    if args.serial is None:
        try:
            profile = config[args.profile]
        except KeyError:
            print(f"# Profile '{args.profile}' not found!")
            profile = setup_profile(config, args.profile)
        try:
            mfa_serial = args.serial or profile["mfa_serial"]
        except KeyError:
            print(
                f"# Profile '{args.profile}' does not have mfa_serial set!")
            profile = setup_profile(config, args.profile)
            mfa_serial = profile["mfa_serial"]
    else:
        mfa_serial = str(args.serial)

    def get_mfa_token():
        """
        This nested function allows repeated input tries on invalid MFA tokens.
        """
        mfa_token = args.token or input(
            "MFA token: ") if args.token is None else str(args.token)
        if not search(r"^\d{6}$", mfa_token):
            print("Please input valid 6-digit MFA token (i.e. 123456)")
            mfa_token = get_mfa_token()
        return mfa_token

    mfa_token = get_mfa_token()

    return (config, profile, args.profile, mfa_serial, mfa_token)


def aws_temp_auth(config, profile, profile_name, mfa_serial, mfa_token):
    """
    According to which profile was chosen, retrieve the temporary authorization credentials using aws CLI command 'sts'.
    Write the credentials data to the AWS profile "temp".
    """
    # An already set but expired AWS_SESSION_TOKEN will make it break, so we remove it first.
    clean_env = os.environ.copy()
    if 'AWS_SESSION_TOKEN' in clean_env:
        print("# Deleting session token", file=sys.stderr)
        del clean_env['AWS_SESSION_TOKEN']

    # Execute STS command to retrieve temporary credentials.
    proc = subprocess.Popen([
        "aws", "sts", "get-session-token",
        "--profile", profile_name,
        "--serial-number", mfa_serial,
        "--token-code", mfa_token,
        '--output', 'json'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=clean_env)
    data, _ = proc.communicate()
    if proc.returncode != 0:
        print("# aws sts get-session-token failed: ",
              data.decode('utf-8'))
        sys.exit(-1)

    # Get the credentials data and create a new "temp" aws credentials profile entry with the data.
    credentials = json.loads(data.decode('utf-8'))["Credentials"]
    setup_profile(config, "temp", credentials["AccessKeyId"],
                  credentials["SecretAccessKey"], credentials["SessionToken"], profile["region"], profile["output"])

    # Ask the user to export the profile-override environment variable to "temp".
    # We can't do this intuitively in this program's execution/memory space; the commented lines below would not work.
    # os.system("export AWS_PROFILE=temp")
    # subprocess.call("export AWS_PROFILE=temp", shell=True)
    # os.environ["AWS_PROFILE"] = "temp"
    print("Please execute the following command: export AWS_PROFILE=temp")


def setup_profile(aws_credentials_file_config, profile_name, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region=None, output=None):
    """
    Create AWS profile for CLI usage.
    Sets configuration within two files: ~/.aws/credentials and ~/.aws/config.
    """
    print(f"Setting up AWS configuration for profile '{profile_name}'")

    # Start setting up the 'credentials' file configuration for the new profile.
    aws_credentials_file_config[profile_name] = {}
    creds_profile = aws_credentials_file_config[profile_name]
    creds_profile["aws_access_key_id"] = aws_access_key_id or input(
        "AWS Access Key ID: ")
    creds_profile["aws_secret_access_key"] = aws_secret_access_key or input(
        "AWS Secret Access Key: ")
    if not aws_session_token:
        creds_profile["mfa_serial"] = input(
            "MFA Device Serial (i.e. arn:aws:iam::<AWS ACCOUNT ID>:mfa/<IAM USER NAME>): ")
    else:
        creds_profile["aws_session_token"] = aws_session_token
    creds_profile["region"] = region or input("Region: ")
    creds_profile["output"] = output or input("Output: ")

    if not aws_session_token and input(f"{json.dumps(dict(creds_profile), indent=4)}\nEverything look alright? (y,n) " == "n"):
        setup_profile(aws_credentials_file_config, profile_name)
    else:
        # Write the aws 'credentials' file with its configuration.
        with open(expanduser("~/.aws/credentials"), "w") as cred_file:
            aws_credentials_file_config.write(cred_file)

        # Start setting up the 'config' file configuration for the new profile.
        aws_config_file_config = configparser.ConfigParser()
        aws_config_file_config.read(expanduser("~/.aws/config"))
        profile_name = f"profile {profile_name}" if profile_name != "default" else profile_name
        aws_config_file_config[profile_name] = {
            "region": creds_profile["region"], "output": creds_profile["output"]}

        # Write the aws 'config' file with its configuration.
        with open(expanduser("~/.aws/config"), "w") as conf_file:
            aws_config_file_config.write(conf_file)

    return creds_profile


def main():
    """
    Meat and potatoes.
    """
    args = parse_args()
    config, profile, profile_name, mfa_serial, mfa_token = validate_args(args)
    aws_temp_auth(config, profile, profile_name, mfa_serial, mfa_token)


if __name__ == "__main__":
    main()
