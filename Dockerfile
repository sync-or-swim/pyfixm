FROM alpine AS journaler

RUN apk add --no-cache \
        python3-dev \
        wget ca-certificates && \
    pip3 install --upgrade pip

WORKDIR /xsd
RUN update-ca-certificates && \
    wget -nv -O core_schema.zip https://www.fixm.aero/releases/FIXM-3.0/FIXM_Core_v3_0_Schemas.zip && \
    wget -nv -O ext_schema.zip https://www.fixm.aero/releases/US_Ext-3.0/FIXM_US_Extension_v3_0_Schemas.zip && \
    unzip core_schema.zip && \
    unzip ext_schema.zip && \
    rm core_schema.zip && \
    rm ext_schema.zip
COPY base_schema.xsd .

WORKDIR /src/
COPY Pipfile .
COPY Pipfile.lock .
RUN pip3 install pipenv && \
    pipenv install --deploy --system --ignore-pipfile

COPY . .
RUN mkdir /pyswim/ && \
#    pyxbgen -m fixm_schema \
#        --schema-location /xsd/base_schema.xsd \
#        --schema-root /xsd/ \
#        --binding-root /pyswim/
    pyxbgen -m fixm_schema \
        --schema-location /xsd/schemas/core/Fixm.xsd \
        --schema-location /xsd/schemas/extensions/nas/Nas.xsd \
        --schema-root /xsd/ \
        --binding-root /pyswim/

WORKDIR /pyswim
RUN touch __init__.py
#RUN python3 /src/test_schema.py
