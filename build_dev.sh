#source activate myenv
cd conda.recipe/
sudo conda build .
sudo conda install --use-local /opt/anaconda/conda-bld/linux-64/py_earthquakes-0.0.3-py27_0.tar.bz2 
cd -
