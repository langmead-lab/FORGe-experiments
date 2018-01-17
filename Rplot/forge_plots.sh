#!/bin/sh

/usr/local/bin/R -e "rmarkdown::render('forge_plots.Rmd',output_file='forge_plots.html')"
