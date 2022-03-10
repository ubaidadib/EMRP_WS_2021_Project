-- Table: public.ta_connection

-- DROP TABLE public.ta_connection;

CREATE TABLE IF NOT EXISTS public.ta_connection
(
    msg_id text COLLATE pg_catalog."default" NOT NULL,
    gateway_id text COLLATE pg_catalog."default" NOT NULL,
    gateway_eui text COLLATE pg_catalog."default",
    time_gateway timestamp with time zone NOT NULL,
    rssi integer,
    channel_rssi integer,
    snr real,
    bandwidth integer,
    spreading_factor integer,
    coding_rate character(8) COLLATE pg_catalog."default",
    consumed_airtime character(9) COLLATE pg_catalog."default",
    topic text COLLATE pg_catalog."default",
    CONSTRAINT ta_connection_pkey PRIMARY KEY (msg_id, time_gateway)
);