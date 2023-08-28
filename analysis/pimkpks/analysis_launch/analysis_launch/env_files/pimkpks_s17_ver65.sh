#!/bin/bash

source /group/halld/Software/build_scripts/gluex_env_jlab.sh
gxenv /group/halld/www/halldweb/html/halld_versions/analysis-2017_01-ver65.xml
export JANA_CALIB_CONTEXT="variation=mc"