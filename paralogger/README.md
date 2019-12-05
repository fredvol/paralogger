# paralogger
This is the main code part of the project.

![3D_view](/doc_for_readme/3D.png?raw=true "3D_view")

## Goals:
* Create a software suite to use the datalogger in the air including:
    *   Graph visualistion
    *   3D reconstruction
    *   view on data
    *   Export capapility for working with other soft
    *   auto sync with Video
    *   Easy delimitation of interesting test sections of teh flight


## Specs:
* Mutiplatform
* able to work headless, on batch of log files
* working as postprocessing, not in live processing


## Environement
developped on linux  (linux mint : 19.2)

python: 3.7
pyqt5: 5.9
pyqtgraph: 0.10
numpy: 1.16
pandas: 0.25

Created it 
* using  conda:

    ```bash
    conda env create -f environment.yml

    ```
* using  pip:

    ```bash
    pip install -r requirements.txt
     ```

## Versioning

We use: git , with LFS : <a href="https://github.com/git-lfs/git-lfs/wiki/Installation">https://github.com/git-lfs/git-lfs/wiki/Installation </a> 

## Overview of the code organisation:

  [![soft mindmap](/doc_for_readme/Paralogger.svg)](https://framindmap.org/c/maps/848541/public "softaware mind map ( V 0.2.0")



## LICENSE
GPL V3

WIP