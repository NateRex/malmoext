# MalmoExt

[![Pipeline Status](https://github.com/NateRex/malmoext/actions/workflows/pipeline.yml/badge.svg?branch=master)](https://github.com/NateRex/malmoext/actions/workflows/pipeline.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

The purpose of this project is to provide a wrapper for Microsoft's [Malmo Platform](https://github.com/microsoft/malmo/tree/master) which provides users a programming interface for creating and running scenarios with minimal effort.

A Python wrapper for Microsoft's [Malmo Platform](https://github.com/microsoft/malmo/tree/master), intended to serve the following purposes:

- Allow for easier installation of Malmo
- Provide a programming interface that streamlines the creation and execution of scenarios.
- Provide a set of higher-order agent actions for developers to choose from.


<br>

## 🔌 Getting Started

Ensure you have the necessary dependencies installed on your machine. The version of Python you need depends on your operating system given Malmo platform requirements.

|Link|Version|
|:---:|:---|
|[Java Development Kit](https://openjdk.org/projects/jdk8/)|<ul>8</ul>|
|[Python](https://www.python.org/downloads/)|<ul><li>3.5.x for Linux</li><li>3.6.x for Windows</li><li>3.7.x for MacOS</li></ul> |

Install the package:

```
pip install malmoext
```

<br>

## 💻 Starting Malmo Minecraft

Malmo Minecraft must be started prior to running a scenario. *<ins>At least</ins> one instance is required for each agent present in your scenario(s).*

To spawn one or more instances of Malmo Minecraft:

```
python -m malmoext --ports 10000 10001 ...
```

Once running, these Malmo Minecraft servers can be reused across multiple scenarios.

<br>

## 🌍 Running a Scenario

Once one or more instances of Malmo Minecraft is running, you can execute one of your scenarios by running its script:

```
python myScenario.py
```

For examples on how to build scenarios, check out the [examples folder](examples).

<br>

## ⚙️ Environment Variables

The following environment variables can optionally be set:

|Name|Default|Description|
|:---|:---|:---|
|`MALMO_INSTALL_DIR`|(the current working directory)|The directory that the Malmo Platform should be installed to when starting Malmo Minecraft for the first time. It is recommended that users set this to a constant value in order to avoid having Malmo installed to multiple locations.|

<br>

## 📃 Additional Documentation

- [API Documentation](https://naterex.github.io/malmoext/)
- [Planned Features](./FEATURES.md)