"""
This script is used to test the dataModels definitions.

Simply call "python test.py" from the project's root if you want to validate all
models or from the folder of the model(s) you want to validate.

Models are recognized by the presence of the "schema.json" file.

Validation is executed using ajv-cli under the hood, and for a model to be valid
it must include an "example.json" file next to the schema. Of course, both
schema and model should be valid as well.

This script will output all errors found in the validation to stdout.
"""
from __future__ import print_function
import json
import os
import re
import subprocess


def get_models_paths(root_dir="."):
    """
    :rtype: list(unicode)
    :returns: List all models in project under CWD. Each "model" here is the
    relative path to model's schema.json file.
    """
    models = []
    for root, dirs, files in os.walk(root_dir):
        if "schema.json" in files:
            models.append(root)
    return models


def get_references(schema_filename):
    """
    :param str schema_filename:
    :returns: set(str)
        All the referenced models in schema_filename.
    """
    refs = set([])

    # TODO: Understand better why these common-schema and geometry-schema jsons
    #       are at the root. Also, how to properly get the files to be
    #       referenced via -r params during validation.
    refs.add('common-schema.json')
    refs.add('geometry-schema.json')

    # TODO: Will we support external references here? How?
    with open(schema_filename, 'r') as sf:
        try:
            schema = json.load(sf)
        except Exception as e:
            # Schema might be invalid, but this should not be treated here.
            import warnings
            msg = "Exception raised when loading references from {}".format(schema_filename)
            warnings.warn(msg)
        else:
            for ao in schema.get("allOf", []):
                if "$ref" in ao:
                    found = re.search("dataModels/.*\.json", ao["$ref"])
                    if found:
                        r = found.group(0).replace("dataModels/", "", 1)
                        refs.add(r)
    return refs


def validate_model(model):
    """
    Validates schema and example of a single model.

    :param: str model
        The "model" is the relative path of the model's schema.json file to be
        validated. e.g : Weather/ObservedWeather
    """
    schema_err = None
    example_err = None

    schema_filename = os.path.join(model, "schema.json")

    # Prepare references params for validator (always relative to project root)
    refs = get_references(schema_filename)
    prefix = (os.path.dirname(str(__file__)) or (".")) + os.sep
    refs_param = "".join(["-r {}{} ".format(prefix,r) for r in refs])

    # Validate schema
    cmd = "ajv compile --v5 -s {schema_filename} {refs_param}".format(
        schema_filename=schema_filename,
        refs_param=refs_param
    )
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        schema_err = "\n".join((str(e.returncode), e.output))
    else:
        # Validate example
        example_filename = os.path.join(model, "example.json")
        cmd = "ajv test --v5 -s {schema_filename} {refs_param} -d {example_filename} --valid".format(
            schema_filename=schema_filename,
            refs_param=refs_param,
            example_filename=example_filename
        )
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            example_err = "\n".join((str(e.returncode), e.output))

    if schema_err or example_err:
        return False

    model_name = (model if model != "." else os.path.basename(os.getcwd()))
    print("{}: OK".format(model_name))
    return True


if __name__ == "__main__":
    models = get_models_paths()
    if models:
        all_valid = True
        for m in models:
            all_valid &= validate_model(m)
        assert all_valid
    else:
        print("No models were found under path {}".format(os.getcwd()))
