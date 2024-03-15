# jay

A simple converter between JSON and YAML.

## Usage

By default, `jay` converts from YAML to JSON:

```
jay /path/to/file.yaml
```

But the other direction is possible:

```
jay --j2y /path/to/file.json
```

It will attempt to read from stdin if there is no file given:

```
cat file.yaml | jay
```

You can specify an output file:

```
jay --output deployment.json deployment.yaml
```

## Notes

This application uses [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) since
it provides better output control than PyYAML, which I appreciate since I have a
particular style in which I like my YAML.
