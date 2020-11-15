FROM alpine AS journaler

RUN apk add --no-cache \
        python3-dev py3-pip \
        wget ca-certificates \
        # For generateDS
        gcc libxslt-dev libxml2 libc-dev && \
    pip install --upgrade pip generateDS==2.36.5

WORKDIR /xsd/
RUN update-ca-certificates && \
    wget -nv -O core_schema.zip https://www.fixm.aero/releases/FIXM-3.0/FIXM_Core_v3_0_Schemas.zip && \
    wget -nv -O ext_schema.zip https://www.fixm.aero/releases/US_Ext-3.0/FIXM_US_Extension_v3_0_Schemas.zip && \
    unzip core_schema.zip && \
    unzip ext_schema.zip && \
    rm core_schema.zip && \
    rm ext_schema.zip
COPY resources/base_schema.xsd .

# Generate XSD Python code
WORKDIR /pyfixm/
RUN generateDS \
    -o /pyfixm/__init__.py \
    -s /pyfixm/subs.py \
    /xsd/base_schema.xsd

# Create the license
WORKDIR /license/
COPY resources/get_license.py .
RUN python3 get_license.py /xsd/schemas/core/base/Base.xsd /pyfixm/LICENSE
