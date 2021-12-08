BEGIN;


CREATE TABLE IF NOT EXISTS public.basket
(
    id integer NOT NULL,
    device_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.brand
(
    id integer NOT NULL,
    type_id integer NOT NULL,
    name character varying(255) NOT NULL,
    country character varying(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.device
(
    id integer NOT NULL,
    price integer NOT NULL,
    type_id integer NOT NULL,
    brand_id integer NOT NULL,
    name character varying(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.type
(
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."user"
(
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    email character varying(255) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public.basket
    ADD FOREIGN KEY (device_id)
    REFERENCES public.device (id)
    NOT VALID;


ALTER TABLE public.basket
    ADD FOREIGN KEY (user_id)
    REFERENCES public."user" (id)
    NOT VALID;


ALTER TABLE public.brand
    ADD FOREIGN KEY (type_id)
    REFERENCES public.type (id)
    NOT VALID;


ALTER TABLE public.device
    ADD FOREIGN KEY (brand_id)
    REFERENCES public.brand (id)
    NOT VALID;


ALTER TABLE public.device
    ADD FOREIGN KEY (type_id)
    REFERENCES public.type (id)
    NOT VALID;

END;
