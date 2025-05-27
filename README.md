# BSA Agent Checker (Python)

Automate your BMC TrueSight Server Automation (BSA) agent port checks and remote service restarts with Python!

## Features

- Checks if port .... is open on each host (RSCD agent connectivity)
- Optionally restarts the RSCD service remotely via WinRM (Windows only)
- Outputs status for each host

## Usage

1. Prepare your host list file (one server name or IP per line):

```
servername01
servername02
serveripAdress
```

2. Install requirements:

```sh
pip install -r requirements.txt
```

3. Run the script:

```sh
python bsa_agent_checker.py hosts.txt --user yourdomain\\youruser --password yourpassword
```

- If you just want to check the port, omit `--user` and `--password`.

## License

MIT License © 2025 Gökhan Yıldırım
