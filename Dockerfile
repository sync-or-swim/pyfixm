FROM alpine AS journaler

RUN apk add --no-cache \
        python3-dev \
        wget ca-certificates \
        # For generateDS
        gcc libxslt-dev libxml2 libc-dev && \
    pip3 install --upgrade pip

WORKDIR /xsd
RUN update-ca-certificates && \
    wget -nv -O core_schema.zip https://www.fixm.aero/releases/FIXM-3.0/FIXM_Core_v3_0_Schemas.zip && \
    wget -nv -O ext_schema.zip https://www.fixm.aero/releases/US_Ext-3.0/FIXM_US_Extension_v3_0_Schemas.zip && \
    unzip core_schema.zip && \
    unzip ext_schema.zip && \
    rm core_schema.zip && \
    rm ext_schema.zip
COPY resources/base_schema.xsd .

WORKDIR /src/
RUN pip3 install generateDS

WORKDIR /pyfixm
RUN generateDS \
    -o /pyfixm/pyfixm.py \
    -s /pyfixm/pyfixm_subs.py \
    ../xsd/base_schema.xsd
