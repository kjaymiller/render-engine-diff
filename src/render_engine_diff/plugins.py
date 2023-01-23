import logging
import filecmp
import datetime
import shutil
import pathlib
import difflib
import pprint
from render_engine.hookspecs import hook_impl


prefix = datetime.datetime.now().strftime("%Y%m%d")

class DirDiff:
    @hook_impl
    def pre_build_site(site):
        if pathlib.Path(site.output_path).is_dir():
            shutil.copytree(site.output_path, f"{prefix}{site.output_path}")
        else:
            logging.warning(f"{site.output_path=} does not exist. Skipping Diff")



    @hook_impl
    def post_build_site(site):
        if pathlib.Path(f"{prefix}{site.output_path}").is_dir():
            diff = filecmp.dircmp(site.output_path, f"{prefix}{site.output_path}")
            for file in diff.diff_files:
                # compare the files
                with open(f"{prefix}{site.output_path}/{file}") as f1:
                    with open(f"{site.output_path}/{file}") as f2:
                        diff = difflib.context_diff(
                            f1.readlines(), f2.readlines(), fromfile=file, tofile=file
                        )
                        pprint.pprint(list(diff))
            shutil.rmtree(f"{prefix}{site.output_path}")
