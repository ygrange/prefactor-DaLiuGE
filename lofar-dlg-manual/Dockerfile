#
# base
#
FROM dlglofar/centos7

RUN sudo yum -y install tmux vim net-tools wget

RUN cd $HOME && mkdir raw_small && cd raw_small && \
    wget ftp://ftp.astron.nl/outgoing/EOSC/datasets/L570745_uv_first10.MS.tar.xz && \
    tar xvf L570745_uv_first10.MS.tar.xz && rm  L570745_uv_first10.MS.tar.xz

ENV MY_IP 10.141.5.97
