from time import sleep
import paramiko
from utils.request import db_request
# from helpers.handlers.printer import log
from utils.decoder import decoder
from utils.definitions import endpoints


def ssh(ip, debugging):
    count = 0
    delay = 0.25
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm = None
    cont = True
    creds = db_request(endpoints["get_creds"], {})
    

    # Handling multiple SSH sessions
    while cont and count <= 2:
        try:
            username = creds["data"][count]["user_name"]
            password = creds["data"][count]["password"]
            # print(username)
            # print(password)
            port = 22
            print(f"trying to connect with {username} @ {ip}", "info")
            conn.connect(ip, port, username, password, timeout=20)
            comm = conn.invoke_shell()
            cont = False
        except paramiko.ssh_exception.AuthenticationException:
            print(f"failed to connect with {username} @ {ip}", "info")
            cont = True
            count += 1
            print(f"retrying to re-connect with {creds['data'][count if count < 3 else 2]['user_name']} @ {ip}", "info")
            continue
        except TimeoutError:
            print(f"failed to connect with {username} @ {ip}", "info")
            cont = True
            count += 1
            print(f"retrying to re-connect with {creds['data'][count if count < 3 else 2]['user_name']} @ {ip}", "info")
            continue
        break

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        comm.send(cmd)
        sleep(delay)
        if debugging:
            print(
                f"""
{cmd}""",
                "info",
            )
        enter()

    def quit_ssh():
        conn.close()

    if ip in ["181.232.180.5", "181.232.180.6", "181.232.180.7"]:
        command("enable")
        command("config")
        command("scroll 512")
    else:
        # command("\n")
        # command("N")
        command("\n")
        command("sys")
    # val = decoder(comm)
    # print(val)
    return (comm, command, quit_ssh)
