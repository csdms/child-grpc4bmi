# A grpc4bmi server for the `CHILD` model.
FROM csdms/grpc4bmi:0.3.0

LABEL org.opencontainers.image.authors="Mark Piper <mark.piper@colorado.edu>"
LABEL org.opencontainers.image.source="https://github.com/csdms/child-grpc4bmi"

RUN git clone --branch v21.03.12 --depth 1 https://github.com/childmodel/child /opt/child
WORKDIR /opt/child/src/_build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=${CONDA_DIR} && \
    make && \
    ctest -V && \
    make install && \
    make clean

COPY server /opt/child-grpc4bmi-server
WORKDIR /opt/child-grpc4bmi-server/_build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=${CONDA_DIR} && \
    make && \
    make install && \
    make clean

WORKDIR /opt

ENTRYPOINT ["/opt/conda/bin/child-grpc4bmi-server"]
EXPOSE 55555
