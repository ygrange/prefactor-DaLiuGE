#
# base
#
FROM dlglofar-base/centos7:latest

#
# common-environment
#
ENV INSTALLDIR /home/${USER}/opt

USER root
#
# environment
#
ENV PYTHON_VERSION 2.7

#
# versions
#
ENV CFITSIO_VERSION 3410
ENV WCSLIB_VERSION 5.19.1
ENV LOG4CPLUS_VERSION 1.1.x
ENV CASACORE_VERSION v2.3.0
ENV PYTHON_CASACORE_VERSION v2.1.2
ENV PYBDSF_VERSION v1.8.11
ENV AOFLAGGER_VERSION v2.8.0
ENV LOFAR_VERSION 2_21_4
ENV WSCLEAN_VERSION 2.4
ENV LOG4CPLUS_VERSION 1.1.x
ENV GCC_VERSION 4.9.3
ENV BOOST_VERSION 1.60.0
ENV HDF5_VERSION 1.10.1
ENV BLAS_VERSION 0.2.17
ENV LAPACK_VERSION 3.6.0
ENV FFTW_VERSION 3.3.4
ENV GSL_VERSION 1.15
ENV XMLRUNNER_VERSION 1.7.7
ENV MONETDB_VERSION 11.19.3.2
ENV UNITTEST2_VERSION 1.1.0
ENV PYFITS_VERSION 3.3
ENV PYWCS_VERSION 1.12

#
# set-uid
#
ENV UID 1024

#
# build environment
#
ENV J 64

#
# base
#
RUN yum -y install automake-devel aclocal autoconf autotools cmake make
RUN yum -y install g++ gcc gcc-c++ gcc-gfortran
RUN yum -y install blas-devel boost-devel fftw3-devel fftw3-libs python-devel lapack-devel libpng-devel libxml2-devel readline-devel ncurses-devel bzip2-devel libicu-devel 
RUN yum -y install bison flex ncurses tar bzip2 which gettext
RUN pip install pyfits pywcs python-monetdb xmlrunner unittest2 scipy matplotlib pp progressbar 
#RUN pip install -U setuptools 

USER ${USER}

#
# install-cfitsio
#
RUN mkdir -p ${INSTALLDIR}/cfitsio/build
RUN cd ${INSTALLDIR}/cfitsio && wget --retry-connrefused ftp://anonymous@heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio${CFITSIO_VERSION}.tar.gz
RUN cd ${INSTALLDIR}/cfitsio && tar xf cfitsio${CFITSIO_VERSION}.tar.gz
RUN cd ${INSTALLDIR}/cfitsio/build && cmake -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/cfitsio/ ../cfitsio
RUN cd ${INSTALLDIR}/cfitsio/build && make -j ${J}
RUN cd ${INSTALLDIR}/cfitsio/build && make install

#
# install-wcslib
#
RUN mkdir ${INSTALLDIR}/wcslib
RUN if [ "${WCSLIB_VERSION}" = "latest" ]; then cd ${INSTALLDIR}/wcslib && wget --retry-connrefused ftp://anonymous@ftp.atnf.csiro.au/pub/software/wcslib/wcslib.tar.bz2 -O wcslib-latest.tar.bz2; fi
RUN if [ "${WCSLIB_VERSION}" != "latest" ]; then cd ${INSTALLDIR}/wcslib && wget --retry-connrefused ftp://anonymous@ftp.atnf.csiro.au/pub/software/wcslib/wcslib-${WCSLIB_VERSION}.tar.bz2; fi
RUN cd ${INSTALLDIR}/wcslib && tar xf wcslib-*.tar.bz2
RUN cd ${INSTALLDIR}/wcslib/wcslib* && ./configure --prefix=${INSTALLDIR}/wcslib --with-cfitsiolib=${INSTALLDIR}/cfitsio/lib/ --with-cfitsioinc=${INSTALLDIR}/cfitsio/include/ --without-pgplot
RUN cd ${INSTALLDIR}/wcslib/wcslib* && make
RUN cd ${INSTALLDIR}/wcslib/wcslib* && make install

#
# install-hdf5
#

RUN mkdir -p ${INSTALLDIR}/hdf5
RUN cd ${INSTALLDIR}/hdf5 && wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-${HDF5_VERSION%.*}/hdf5-${HDF5_VERSION}/src/hdf5-${HDF5_VERSION}.tar.gz
RUN cd ${INSTALLDIR}/hdf5 && tar xf hdf5*.tar.gz
RUN cd ${INSTALLDIR}/hdf5/hdf5*/ && ./configure --prefix=${INSTALLDIR}/hdf5 --enable-fortran --enable-threadsafe --enable-cxx --with-pthread --enable-linux-lfs --enable-unsupported
RUN cd ${INSTALLDIR}/hdf5/hdf5*/ && make -j ${J}
RUN cd ${INSTALLDIR}/hdf5/hdf5*/ && make install

#
# install-casacore
#
RUN mkdir -p ${INSTALLDIR}/casacore/build
RUN mkdir -p ${INSTALLDIR}/casacore/data
RUN cd ${INSTALLDIR}/casacore && git clone https://github.com/casacore/casacore.git src
RUN if [ "${CASACORE_VERSION}" != "latest" ]; then cd ${INSTALLDIR}/casacore/src && git checkout tags/${CASACORE_VERSION}; fi
RUN cd ${INSTALLDIR}/casacore/data && wget --retry-connrefused ftp://anonymous@ftp.astron.nl/outgoing/Measures/WSRT_Measures.ztar
RUN cd ${INSTALLDIR}/casacore/data && tar xf WSRT_Measures.ztar
RUN cd ${INSTALLDIR}/casacore/build && cmake -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/casacore/ -DDATA_DIR=${INSTALLDIR}/casacore/data -DWCSLIB_ROOT_DIR=/${INSTALLDIR}/wcslib/ -DCFITSIO_ROOT_DIR=${INSTALLDIR}/cfitsio/ -DBUILD_PYTHON=True -DUSE_OPENMP=True -DUSE_FFTW3=TRUE -DHDF5_ROOT_DIR=${INSTALLDIR}/hdf5 -DUSE_HDF5=True ../src/ 
RUN cd ${INSTALLDIR}/casacore/build && make -j ${J}
RUN cd ${INSTALLDIR}/casacore/build && make install

#
# install-python-casacore
#
RUN mkdir ${INSTALLDIR}/python-casacore
RUN cd ${INSTALLDIR}/python-casacore && git clone https://github.com/casacore/python-casacore
RUN if [ "$PYTHON_CASACORE_VERSION" != "latest" ]; then cd ${INSTALLDIR}/python-casacore/python-casacore && git checkout tags/${PYTHON_CASACORE_VERSION}; fi
RUN cd ${INSTALLDIR}/python-casacore/python-casacore && ./setup.py build_ext -I${INSTALLDIR}/wcslib/include:${INSTALLDIR}/casacore/include/:${INSTALLDIR}/cfitsio/include -L${INSTALLDIR}/wcslib/lib:${INSTALLDIR}/casacore/lib/:${INSTALLDIR}/cfitsio/lib/ -R${INSTALLDIR}/wcslib/lib:${INSTALLDIR}/casacore/lib/:${INSTALLDIR}/cfitsio/lib/
RUN mkdir -p ${INSTALLDIR}/python-casacore/lib/python${PYTHON_VERSION}/site-packages/
RUN mkdir -p ${INSTALLDIR}/python-casacore/lib64/python${PYTHON_VERSION}/site-packages/
RUN export PYTHONPATH=${INSTALLDIR}/python-casacore/lib/python${PYTHON_VERSION}/site-packages:${INSTALLDIR}/python-casacore/lib64/python${PYTHON_VERSION}/site-packages:$PYTHONPATH && cd ${INSTALLDIR}/python-casacore/python-casacore && ./setup.py develop --prefix=${INSTALLDIR}/python-casacore/

#
# install-aoflagger
#
RUN mkdir -p ${INSTALLDIR}/aoflagger/build
RUN cd ${INSTALLDIR}/aoflagger && git clone git://git.code.sf.net/p/aoflagger/code aoflagger
RUN cd ${INSTALLDIR}/aoflagger/aoflagger && git checkout tags/${AOFLAGGER_VERSION}
RUN cd ${INSTALLDIR}/aoflagger/build && cmake -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/aoflagger/ -DCASACORE_ROOT_DIR=${INSTALLDIR}/casacore -DCFITSIO_ROOT_DIR=${INSTALLDIR}/cfitsio -DBUILD_SHARED_LIBS=ON ../aoflagger
RUN cd ${INSTALLDIR}/aoflagger/build && make -j ${J}
RUN cd ${INSTALLDIR}/aoflagger/build && make install

#
# install-log4cplus
#
RUN mkdir -p ${INSTALLDIR}/log4cplus/build
RUN cd ${INSTALLDIR}/log4cplus && git clone https://github.com/log4cplus/log4cplus.git -b ${LOG4CPLUS_VERSION} src
RUN cd ${INSTALLDIR}/log4cplus/build && cmake -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/log4cplus ../src/
RUN cd ${INSTALLDIR}/log4cplus/build && make -j ${J}
RUN cd ${INSTALLDIR}/log4cplus/build && make install

#
# install-lofar
#
RUN mkdir -p ${INSTALLDIR}/lofar/build/gnu_opt
RUN if [ "${LOFAR_VERSION}" = "latest" ]; then cd ${INSTALLDIR}/lofar && svn --non-interactive -q co https://svn.astron.nl/LOFAR/trunk src; fi
RUN if [ "${LOFAR_VERSION}" != "latest" ]; then cd ${INSTALLDIR}/lofar && svn --non-interactive -q co https://svn.astron.nl/LOFAR/tags/LOFAR-Release-${LOFAR_VERSION} src; fi
RUN cd ${INSTALLDIR}/lofar/build/gnu_opt && cmake -DBUILD_PACKAGES="pyparmdb BBSKernel BBSControl pystationresponse DP3 GSM Pipeline ExpIon" -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/lofar/ -DWCSLIB_ROOT_DIR=${INSTALLDIR}/wcslib/ -DCFITSIO_ROOT_DIR=${INSTALLDIR}/cfitsio/ -DCASACORE_ROOT_DIR=${INSTALLDIR}/casacore/ -DAOFLAGGER_ROOT_DIR=${INSTALLDIR}/aoflagger/ -DLOG4CPLUS_ROOT_DIR=${INSTALLDIR}/log4cplus/ -DHDF5_ROOT_DIR=${INSTALLDIR}/hdf5 -DUSE_OPENMP=True ${INSTALLDIR}/lofar/src/
RUN cd ${INSTALLDIR}/lofar/build/gnu_opt && make install

#
# wsclean
# 
RUN sudo yum install -y gsl-devel && \
    CPATH=${INSTALLDIR}/casacore/include/casacore:$CPATH && \
    mkdir -p ${INSTALLDIR}/wsclean/build && \
    cd ${INSTALLDIR}/wsclean && \
    wget http://downloads.sourceforge.net/project/wsclean/wsclean-${WSCLEAN_VERSION}/wsclean-${WSCLEAN_VERSION}.tar.bz2 && \
    tar xf wsclean-${WSCLEAN_VERSION}.tar.bz2 && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=${INSTALLDIR}/wsclean -DCMAKE_PREFIX_PATH="${INSTALLDIR}/lofar;${INSTALLDIR}/casacore;${INSTALLDIR}/cfitsio/" -DBUILD_SHARED_LIBS=TRUE ../wsclean-${WSCLEAN_VERSION} && \
    make -j  && \
    make install 

ENV LSMTOOL_VERSION v1.2.0
ENV RMEXTRACT_VERSION v0.1 
ENV LOSOTO_VERSION 1.0.1
ENV PREFACTOR_VERSION V2.0.2

# *******************
#   LSMTool
# *******************

RUN cd ${INSTALLDIR} && git clone https://github.com/darafferty/LSMTool.git && \
    if [ "$LSMTOOL_VERSION" != "latest" ]; then cd ${INSTALLDIR}/LSMTool && git checkout tags/${LSMTOOL_VERSION}; fi && \ 
    mkdir -p /home/${USER}/opt/prefactor-reqs/lib/python2.7/site-packages/ && \
    export PYTHONPATH=${PYTHONPATH}:${INSTALLDIR}/prefactor-reqs/lib/python2.7/site-packages/ && \
    cd ${INSTALLDIR}/LSMTool && sed -i.bak 's/astropy >= 0.4/astropy >= 0.4, <3.0/g' setup.py && \
    python setup.py install --prefix=${INSTALLDIR}/prefactor-reqs

# *******************
#   RMExtract
# *******************
RUN cd ${INSTALLDIR} && git clone https://github.com/lofar-astron/RMextract.git && \
    if [ "$RMEXTRACT_VERSION" != "latest" ]; then cd ${INSTALLDIR}/RMextract && git checkout tags/${RMEXTRACT_VERSION}; fi && \
    mkdir -p ${INSTALLDIR}/prefactor-reqs/lib64/python2.7/site-packages/ && \
    export PYTHONPATH=${PYTHONPATH}:${INSTALLDIR}/prefactor-reqs/lib64/python2.7/site-packages/ && \ 
    cd ${INSTALLDIR}/RMextract && python setup.py install --add-lofar-utils --prefix=${INSTALLDIR}/prefactor-reqs

# *******************
#   LoSoTo
# *******************

RUN cd ${INSTALLDIR} && git clone https://github.com/revoltek/losoto.git && \
    export HDF5_DIR=${INSTALLDIR}/hdf5 && \
    if [ "$LOSOTO_VERSION" != "latest" ]; then cd ${INSTALLDIR}/losoto && git checkout tags/${LOSOTO_VERSION}; fi  && \
    export PYTHONPATH=${PYTHONPATH}:${INSTALLDIR}/prefactor-reqs/lib/python2.7/site-packages/ && \
    cd ${INSTALLDIR}/losoto && \
    python setup.py install --prefix=${INSTALLDIR}/prefactor-reqs


# *******************
#   Prefactor
# *******************
RUN cd ${INSTALLDIR} && git clone https://github.com/lofar-astron/prefactor.git && \
    if [ "$PREFACTOR_VERSION" != "latest" ]; then cd ${INSTALLDIR}/prefactor && git checkout tags/${PREFACTOR_VERSION}; fi

#
# init-lofar
#
RUN sudo sh -c 'echo source \${INSTALLDIR}/lofar/lofarinit.sh  >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PYTHONPATH=\${PYTHONPATH:+:\${PYTHONPATH}}:\${INSTALLDIR}/python-casacore/lib/python2.7/site-packages/  >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PYTHONPATH=\${PYTHONPATH:+:\${PYTHONPATH}}:\${INSTALLDIR}/prefactor-reqs/lib/python2.7/site-packages/ >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PYTHONPATH=\${PYTHONPATH:+:\${PYTHONPATH}}:\${INSTALLDIR}/prefactor-reqs/lib64/python2.7/site-packages/ >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PYTHONPATH=\${PYTHONPATH:+:\${PYTHONPATH}}:\${INSTALLDIR}/prefactor/lib/python2.7/site-packages/ >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PYTHONPATH=\${PYTHONPATH:+:\${PYTHONPATH}}:\${INSTALLDIR}/prefactor/scripts >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PATH=\${PATH:+:\${PATH}}:\${INSTALLDIR}/prefactor/scripts >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PATH=\${PATH:+:\$PATH}:\${INSTALLDIR}/casacore/bin:${INSTALLDIR}/wsclean/bin  >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PATH=\${PATH:+:\$PATH}:\${INSTALLDIR}/losoto/bin >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}:\${INSTALLDIR}/casacore/lib  >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}:\${INSTALLDIR}/hdf5/lib >> /usr/bin/init-lofar.sh'
RUN sudo sh -c 'echo export PATH=\${PATH:+:\${PATH}}:\${INSTALLDIR}/wsclean/bin >> /usr/bin/init-lofar.sh'
RUN sudo sh -c "echo source /usr/bin/init-lofar.sh >> /usr/bin/init.sh"

COPY scripts/losoto_importer_wrapper.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/CopyGather.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/calibcal.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/flagave.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/lofar_helpers.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/dlg_lofar.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/losoto_amp_wrap.py  ${INSTALLDIR}/prefactor/scripts
COPY scripts/losoto_clocktecfit.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/examine_npy_dlg.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/wrap_losoto.py ${INSTALLDIR}/prefactor/scripts
COPY scripts/lofar_parsets ${INSTALLDIR}/prefactor/scripts/lofar_parsets
RUN sudo chown ${USER}:${USER} ${INSTALLDIR}/prefactor/scripts/* 

#
# entrypoint
#
ENTRYPOINT /bin/bash --init-file /usr/bin/init.sh

