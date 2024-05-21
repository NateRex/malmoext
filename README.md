# MalmoExt

The purpose of this project is to provide a wrapper for Microsoft's [Malmo Platform](https://github.com/microsoft/malmo/tree/master) which provides users a programming interface for creating and running scenarios with minimal effort.


## Getting Started

Ensure you have the following installed on your machine:

|Link|Version|
|:---:|:---|
|[Python](https://www.python.org/downloads/)|3.6.x|
|[Java Development Kit](https://openjdk.org/projects/jdk8/)|8|

Install the package:

```
pip install malmoext
```

## Starting Malmo Minecraft

Prior to running a scenario, instances of Malmo Minecraft must be started. *At least one instance is required for each agent present in your scenario(s).*

To spawn one or more instances of Malmo Minecraft:

```
python -m malmoext --ports 10000 10001 ...
```

## Running a Scenario

Once one or more instances of Malmo Minecraft is running, you can execute one of your scenarios by running its script:

```
python myScenario.py
```

## Environment Variables

The following environment variables can optionally be set:

|Name|Default|Description|
|:---|:---|:---|
|`MALMO_INSTALL_DIR`|(the current working directory)|The directory that the Malmo Platform should be installed to when starting Malmo Minecraft for the first time. It is recommended that users set this to a constant value in order to avoid having Malmo installed to multiple locations.|

