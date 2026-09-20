import importlib
import pkgutil
import sys

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

base_package = "app.modules"
for module_info in pkgutil.walk_packages([base_package.replace(".", "/")], prefix=f"{base_package}."):
    if ".models." in module_info.name or module_info.name.endswith(".models"):
        print(module_info.name)
