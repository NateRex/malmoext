# MalmoExt Features

This document contains a checklist of the currently planned features for this library. Checked items imply that the feature has already been added.

This document is not guaranteed to be a comprehensive of all changes planned. It is simply meant to serve as a general roadmap of capabilities that have been highly-requested so far.


### General

- [x] Include a main method in this library that is capable of installing and running Malmo Minecraft instances, preventing users from having to install Malmo separately.

- [ ] Automatically generate a machine-readable log of agent actions and effects upon scenario completion.

### Scenario Creation

- [ ] Scenario builder supports Malmo's native construction of a scenario using XML, as an alternative to using the other builder methods

- [x] Scenario builder supports programmatic definition of mission metadata

- [x] Scenario builder supports programmatic construction of all shapes supported natively by Malmo.

- [x] Scenario builder supports programmatic construction of one or more agents.

- [x] Scenario builder supports programmatic manipulation of starting agent inventories.

- [x] Scenario builder supports programmatic manipulations to mob and item spawning.

- [ ] Scenario builder supports programmatic choice between flat and normal world generation.

- [ ] Scenario builder supports programmatic definition of agent rewards

### Scenario State

- [x] Agent state contains agent metadata information

- [x] Agent state contains inventory information

- [x] Agent state contains information on nearby entities

- [x] Agent state contains information on nearby blocks

- [ ] Agent state contains historical information for the agent (such as distance walked, mobs killed, and rewards received for their actions).

### Agent Actions

- [x] Agent supports the execution of native Malmo commands, as an alternative to using the other agent methods representing "higher-order" actions

- [x] Agent can equip an item by type

- [x] Agent can look at another entity

- [x] Agent can move to another entity (no obstacles)

- [ ] Agent can attack another entity

- [ ] Agent can pick up an item

- [ ] Agent can give an item to another entity

- [ ] Agent can mine a block

- [ ] Agent can place a block/item

- [ ] Agent can move to another entity (with obstacles)