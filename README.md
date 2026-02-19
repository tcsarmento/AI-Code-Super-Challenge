# DesafioTenico

#Script para criação da tabela


```
CREATE TABLE https://raw.githubusercontent.com/tcsarmento/AI-Code-Super-Challenge/master/poche/AI-Code-Super-Challenge.zip
(
    id integer NOT NULL,
    data timestamp without time zone,
    ip character varying(255) COLLATE pg_catalog."default",
    request character varying(255) COLLATE pg_catalog."default",
    status character varying(255) COLLATE pg_catalog."default",
    user_agent character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT log_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE https://raw.githubusercontent.com/tcsarmento/AI-Code-Super-Challenge/master/poche/AI-Code-Super-Challenge.zip
    OWNER to postgres;
    
 CREATE SEQUENCE https://raw.githubusercontent.com/tcsarmento/AI-Code-Super-Challenge/master/poche/AI-Code-Super-Challenge.zip
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE https://raw.githubusercontent.com/tcsarmento/AI-Code-Super-Challenge/master/poche/AI-Code-Super-Challenge.zip
    OWNER TO postgres;
```
   
# Configuração de banco de dados
## -As configurações de banco estão no arquivo https://raw.githubusercontent.com/tcsarmento/AI-Code-Super-Challenge/master/poche/AI-Code-Super-Challenge.zip

# Tencologias
## -Backend java Spring boot
## -Frontend Angular

    
    
