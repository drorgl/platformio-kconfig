Import("env")
import subprocess
import os

subprocess.run("pip -q install kconfiglib windows-curses")

if os.name == 'nt':
    subprocess.run("pip -q install kconfiglib")

def menuconfig_callback(*arg, **kwargs):
    save_settings = env.GetProjectOption("custom_kconfig_save_settings", "");
    output_header_file = env.GetProjectOption("custom_kconfig_output_header", "")
    comment_header = env.GetProjectOption("custom_kconfig_comment_header", "")
    config_file = env.GetProjectOption("custom_kconfig_config", "");

    comment = [line.strip() for line in comment_header.splitlines()]
    comment = [line for line in comment if line]
    print("Executing kconfig",config_file,save_settings, output_header_file )
    
    envlist = dict(os.environ)
    envlist["KCONFIG_CONFIG"] = save_settings
    envlist["KCONFIG_CONFIG_HEADER"] = "#" + "\n#".join(comment) + "\n"
    envlist["KCONFIG_AUTOHEADER"] = output_header_file
    envlist["KCONFIG_AUTOHEADER_HEADER"] = "// " + "\n// ".join(comment) + "\n"

    if os.name == 'nt':
        subprocess.call(["menuconfig", config_file], env=envlist, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.call(["menuconfig", config_file], env=envlist)

    genconfig_command = ["genconfig", "--header-path", output_header_file, config_file];
    print(" ".join(genconfig_command))
    subprocess.call(genconfig_command, env=envlist)
 

env.AddCustomTarget(
    "kconfig",
    None,
    menuconfig_callback,
    title="kconfig",
    description="Executes kconfig")

