from dynaconf import Dynaconf

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

settings = Dynaconf(
    envvar_prefix="APPLICATION",
    settings_files=['settings.toml', '.secrets.toml'],
)
