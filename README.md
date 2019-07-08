# DesafioTenico

#Script para criação da tabela


```
CREATE TABLE public.log
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

ALTER TABLE public.log
    OWNER to postgres;
```
   
# Configuração de banco de dados
## -As configurações de banco estão no arquivo ConfiguracaoBanco.java

# Tencologias
## -Backend java Spring boot
## -Frontend Angular

    
    
