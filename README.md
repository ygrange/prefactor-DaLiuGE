# Prefactor dockerfile for DaLiuGE demonstration
Docker files to create a running copy of the LOFAR software including the prefactor pipeline and the awimager. This also includes (or will include) wrapper scripts around the python scripts in the prefactor. 

To run a command in one of the containers, use the syntax as listed on the lofar dockerhub page: 

docker run --rm -u $(id -u) -e USER=$USER -e HOME=$HOME -v $HOME:$HOME lofar-pipeline '<your-command> <arguments>'

The requirement is that the DaLiuGE docker containers are available on the system.
