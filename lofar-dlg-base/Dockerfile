#
# base
#
FROM  dfms/centos7:latest

#
# common-environment
#
ENV USER lofar-dlg

#
# set-uid
#
ENV UID 1024

# base
#
RUN yum -y remove iputils
RUN yum -y update
RUN yum -y install sudo
RUN yum -y install git svn wget 

#
# setup-account
#
RUN getent group sudo &>/dev/null || groupadd sudo
RUN useradd -m -u ${UID} ${USER}
RUN usermod -a -G sudo ${USER}
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN sed -i 's/requiretty/!requiretty/g' /etc/sudoers

USER ${USER}

