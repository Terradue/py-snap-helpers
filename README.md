# py-snap-helpers - functions to build and process SNAP Graphs

## About SNAP

The Sentinel Application Platform - or SNAP - in short is a collection of executable tools and Application Programming Interfaces (APIs) which have been developed to facilitate the utilisation, viewing and processing of a variety of remotely sensed data. The functionality of SNAP is accessed through the Sentinel Toolbox. The purpose of the Sentinel Toolbox is not to duplicate existing commercial packages, but to complement them with functions dedicated to the handling of data products of earth observing satellites.

The main components of the Sentinel Toolbox are:

- An intuitive desktop application used for EO data visualisation, analysing and processing.
- A set of scientific data processors running either from the command-line or invoked by the desktop application.
- The command-line tool gpt (graph processing tool) is used to execute processing graphs made up of operators nodes developed using the SNAP GPF.
- A data product converter tool pconvert allowing a user to convert raw data products to the BEAM-DIMAP standard format, to GeoTIFF, to HDF-5 or to RGB images.
- A Java™ API which provides ready-to-use components for remote sensing related application development and plug-in points for new SNAP extension modules. Besides a number of extension points such as product reader and writers, the SNAP API comprises the Graph Processing Framework (GPF) which is used to rapidly create raster data processors. The Rich Client Platform is used to develop rich GUI user interface applications based on SNAP.

## The SNAP Graph Processing Framework (GPF)

Within SNAP, the term data processor refers to a software module which creates an output product from one or more input products configured by a set of processing parameters. A product is basically a collection of bands which again provide numerical raster data for a spectral radiance, geophysical property or quality flag.

As its name states, the GPF allows to construct directed, acyclic graphs (DAG) of processing nodes. A node in the graph refers to a GPF operator, which implements the algorithm to be executed. The node also has the role to configure the operation by specifying the operator's source nodes and providing values for the processing parameters.

## py-snap-helpers

py-snap-helpers is a set of functions and classes to ease the construction of the SNAP Graphs and trigger their execution.

## Installation

Use conda to install py-snap-helpers:

```bash
conda install -y -c terradue py_snap_helpers
```

or if using a conda environment:

```bash
conda install -y -c terradue -n <environment name> py_snap_helpers
```

### Example

See the Jupyter notebook under the folder **examples**

